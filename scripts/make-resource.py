import subprocess
import argparse
import sys
import re
import json
import fnmatch
import tempfile
import shutil
import platform
from pathlib import Path


def get_rcc_bin():
    is_windows = platform.system() == 'Windows'
    local_base = Path(__file__).parent / 'tools' / 'rcc'

    if is_windows:
        if local_base.exists():
            return str(local_base)
        if local_base.with_suffix('.exe').exists():
            return str(local_base.with_suffix('.exe'))

    if not is_windows:
        for p in ['/usr/bin/rcc', '/usr/bin/rcc-qt5', '/usr/bin/rcc5']:
            if Path(p).exists():
                return p

        local_linux = Path(__file__).parent / 'tools' / 'rcc'
        if local_linux.exists():
            return str(local_linux)

    for name in ['rcc', 'rcc-qt5', 'rcc5', 'rcc-qt6', 'qt6-rcc', 'rcc6']:
        found = shutil.which(name)
        if found:
            return found

    return None


def optimize_svg(content):
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'<metadata>.*?</metadata>', '', content, flags=re.DOTALL)
    content = re.sub(r'<title>.*?</title>', '', content, flags=re.DOTALL)
    content = re.sub(r'<desc>.*?</desc>', '', content, flags=re.DOTALL)
    content = re.sub(r'<g(?:\s[^>]*)?>\s*</g>', '', content, flags=re.DOTALL)
    content = re.sub(r'\b(\d+\.\d{2,})\b', lambda m: format(float(m.group(1)), '.1f'), content)
    content = re.sub(r'\s+', ' ', content).strip()
    return content


def main():
    parser = argparse.ArgumentParser(description='Helper to create qBittorrent themes')
    parser.add_argument('-output', type=str, help='Output .qbtheme file', default='style.qbtheme')
    parser.add_argument('-style', type=Path, help='Path to QSS stylesheet', required=True)
    parser.add_argument('-base-dir', type=Path, dest='baseDir', default='.', help='Base directory for resources')
    parser.add_argument('-icons-dir', type=Path, dest='iconsDir', help='Directory containing custom icons')
    parser.add_argument('-dir-prefix', type=str, default='/uitheme', dest='dirPrefix')
    parser.add_argument('-config', type=Path, dest='config', help='Path to config.json')
    parser.add_argument('-variables', type=Path, dest='variables', help='Path to variables.json for QSS substitution')
    parser.add_argument('-find-files', action='store_true', dest='findFiles', help='Only include files referenced in QSS')
    parser.add_argument('files', nargs='*', default=['*'], help='File patterns to include (relative to base-dir)')

    args = parser.parse_args()

    output_path = Path(args.output)
    if output_path.suffix != '.qbtheme':
        output_path = output_path.with_suffix('.qbtheme')

    if output_path.exists():
        print(f"WARNING: {output_path} exists. Overwriting.")

    stylesheet_path = args.style if args.style.is_absolute() else (args.baseDir / args.style)
    config_path = None
    if args.config:
        config_path = args.config if args.config.is_absolute() else (args.baseDir / args.config)

    icons_path = None
    if args.iconsDir:
        icons_path = args.iconsDir if args.iconsDir.is_absolute() else (args.baseDir / args.iconsDir)

    variables_path = None
    if args.variables:
        variables_path = args.variables if args.variables.is_absolute() else (args.baseDir / args.variables)

    all_potential_files = []
    if args.baseDir.exists():
        for f in args.baseDir.rglob('*'):
            if f.is_file():
                if f.resolve() == stylesheet_path.resolve():
                    continue
                if config_path and f.resolve() == config_path.resolve():
                    continue
                if variables_path and f.resolve() == variables_path.resolve():
                    continue
                if icons_path and icons_path.resolve() in f.resolve().parents:
                    continue
                if f.name == 'LICENSE':
                    continue
                all_potential_files.append(f)

    patterns = args.files
    if args.findFiles:
        print("Finding files referenced in QSS...")
        try:
            stylesheet_content = stylesheet_path.read_text()
            patterns = re.findall(r':/uitheme/([^)]+)', stylesheet_content)
        except Exception as e:
            print(f"Error reading stylesheet: {e}")
            sys.exit(1)

    resource_files = []
    for f in all_potential_files:
        alias = f.relative_to(args.baseDir)
        for p in patterns:
            if fnmatch.fnmatch(str(alias), p):
                resource_files.append((alias, f))
                print(f"Adding {f}")
                break

    icon_files = []
    if icons_path and icons_path.exists():
        icon_files = [f for f in icons_path.rglob('*') if f.is_file()]

    temp_files = []
    temp_dirs = []
    temp_qrc = None

    if variables_path and variables_path.exists():
        try:
            with variables_path.open('r') as f:
                vars_dict = json.load(f)

            content = stylesheet_path.read_text(encoding='utf-8')

            found_vars = re.findall(r'{{([^{}]+)}}', content)
            missing_vars = [v for v in found_vars if v not in vars_dict]
            if missing_vars:
                print(f"ERROR: Missing variables in {args.variables}: {', '.join(set(missing_vars))}")
                sys.exit(1)

            for k, v in vars_dict.items():
                content = content.replace(f'{{{{{k}}}}}', v)

            tf = tempfile.NamedTemporaryFile(mode='w', suffix='.qss', delete=False, encoding='utf-8')
            tf.write(content)
            stylesheet_to_include = Path(tf.name)
            tf.close()
            temp_files.append(stylesheet_to_include)
            print(f"Applied and validated variables from {args.variables}")

            temp_config = None
            if config_path and config_path.exists():
                config_content = config_path.read_text(encoding='utf-8')
                for k, v in vars_dict.items():
                    config_content = config_content.replace(f'{{{{{k}}}}}', v)
                tf2 = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8')
                tf2.write(config_content)
                config_to_include = Path(tf2.name)
                tf2.close()
                temp_files.append(config_to_include)
                print(f"Applied variables to config.json")
            else:
                config_to_include = config_path

            if icon_files:
                td = tempfile.TemporaryDirectory()
                temp_dirs.append(td)
                temp_icons_dir = Path(td.name)

                processed_icons = []
                for icon in icon_files:
                    if icon.suffix == '.svg':
                        content = icon.read_text(encoding='utf-8')
                        content = optimize_svg(content)

                        if '<svg' in content and 'fill=' not in content.split('>')[0]:
                            content = content.replace('<svg ', f'<svg fill="{vars_dict.get("TEXT_PRIMARY", "#ffffff")}" ')

                        content = content.replace('fill="#000000"', f'fill="{vars_dict.get("TEXT_PRIMARY", "#ffffff")}"')
                        content = content.replace('fill="#000"', f'fill="{vars_dict.get("TEXT_PRIMARY", "#ffffff")}"')
                        content = content.replace('fill:black', f'fill:{vars_dict.get("TEXT_PRIMARY", "#ffffff")}')
                        content = content.replace('fill:#000000', f'fill:{vars_dict.get("TEXT_PRIMARY", "#ffffff")}')

                        for k, v in vars_dict.items():
                            content = content.replace(f'{{{{{k}}}}}', v)

                        temp_icon = temp_icons_dir / icon.name
                        temp_icon.write_text(content, encoding='utf-8')
                        processed_icons.append(temp_icon)
                    else:
                        processed_icons.append(icon)
                icon_files = processed_icons
                print(f"Applied variables and optimization to {len(icon_files)} icons")

        except Exception as e:
            print(f"Error applying variables: {e}")
            sys.exit(1)
    else:
        stylesheet_to_include = stylesheet_path
        config_to_include = config_path

    try:
        temp_qrc = tempfile.NamedTemporaryFile(mode='w', suffix='.qrc', delete=False, encoding='utf-8')
        qrc_path = Path(temp_qrc.name)
        qrc_path.write_text('', encoding='utf-8')

        with qrc_path.open('w', encoding='utf-8') as qrc:
            qrc.write('<!DOCTYPE RCC><RCC version="1.0">\n')
            qrc.write('\t<qresource>\n')

            qrc.write(f"\t\t<file alias='stylesheet.qss'>{stylesheet_to_include.resolve()}</file>\n")
            qrc.write(f"\t\t<file alias='style.qss'>{stylesheet_to_include.resolve()}</file>\n")
            if config_to_include and config_to_include.exists():
                qrc.write(f"\t\t<file alias='config.json'>{config_to_include.resolve()}</file>\n")

            for alias, path in resource_files:
                alias_str = str(alias).replace('\\', '/')
                qrc.write(f"\t\t<file alias='{alias_str}'>{path.resolve()}</file>\n")

            for icon in icon_files:
                qrc.write(f"\t\t<file alias='icons/{icon.name}'>{icon.resolve()}</file>\n")

            qrc.write('\t</qresource>\n')
            qrc.write('</RCC>')

        temp_qrc.close()

        rcc_bin = get_rcc_bin()
        if not rcc_bin:
            print("Error: rcc not found. Please install Qt development tools.")
            sys.exit(1)

        cmd = [rcc_bin, '-binary', '-o', str(output_path), str(qrc_path)]
        print(f"Executing: {' '.join(cmd)}")

        ret = subprocess.call(cmd)
        if ret == 0:
            print(f"Successfully built {output_path} using {rcc_bin}")
        else:
            print(f"RCC failed with exit code {ret}")
            sys.exit(1)

    except Exception as e:
        print(f"Error during build: {e}")
        sys.exit(1)
    finally:
        for p in temp_files:
            if p.exists():
                p.unlink()
        for td in temp_dirs:
            td.cleanup()
        if temp_qrc:
            qrc_p = Path(temp_qrc.name)
            if qrc_p.exists():
                qrc_p.unlink()
            if not temp_qrc.closed:
                temp_qrc.close()


if __name__ == '__main__':
    main()
