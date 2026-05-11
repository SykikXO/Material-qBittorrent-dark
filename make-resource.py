import subprocess
import argparse
import sys
import re
import platform
import shutil
from pathlib import Path

def get_rcc_bin():
    is_windows = platform.system() == 'Windows'
    local_base = Path(__file__).parent / 'tools' / 'rcc'
    
    if is_windows:
        if local_base.exists(): 
            return str(local_base)
        if local_base.with_suffix('.exe').exists(): 
            return str(local_base.with_suffix('.exe'))
    
    # Check system PATH
    for name in ['rcc', 'rcc-qt5', 'rcc-qt6']:
        found = shutil.which(name)
        if found: 
            return found
        
    # Fallback for Linux if binary is in tools/
    if not is_windows and local_base.exists():
        return str(local_base)
        
    return None

def main():
    parser = argparse.ArgumentParser(description='Helper to create qBittorrent themes')
    parser.add_argument('-output', type=str, help='Output .qbtheme file', default='style.qbtheme')
    parser.add_argument('-style', type=Path, help='Path to QSS stylesheet', required=True)
    parser.add_argument('-base-dir', type=Path, dest='baseDir', default='.', help='Base directory for resources')
    parser.add_argument('-icons-dir', type=Path, dest='iconsDir', help='Directory containing custom icons')
    parser.add_argument('-dir-prefix', type=str, default='', dest='dirPrefix', help='Prefix added to all files')
    parser.add_argument('-config', type=Path, dest='config', help='Path to config.json')
    parser.add_argument('-find-files', action='store_true', dest='findFiles', help='Only include files referenced in QSS')
    parser.add_argument('files', nargs='*', default=['*'], help='File patterns to include (relative to base-dir)')

    args = parser.parse_args()

    output_path = Path(args.output)
    if output_path.suffix != '.qbtheme':
        output_path = output_path.with_suffix('.qbtheme')

    if output_path.exists():
        print(f"WARNING: {output_path} exists. Overwriting.")

    # Find all files in base directory
    all_potential_files = []
    if args.baseDir.exists():
        for f in args.baseDir.rglob('*'):
            if f.is_file():
                all_potential_files.append(f)

    # Determine which files to include
    patterns = args.files
    if args.findFiles:
        print("Finding files referenced in QSS...")
        try:
            stylesheet_path = args.style if args.style.is_absolute() else (args.baseDir / args.style)
            stylesheet_content = stylesheet_path.read_text()
            # Handle :/uitheme/ paths in QSS
            patterns = re.findall(r':/uitheme/([^)]+)', stylesheet_content)
        except Exception as e:
            print(f"Error reading stylesheet: {e}")
            sys.exit(1)

    resource_files = []
    for f in all_potential_files:
        alias = f.relative_to(args.baseDir)
        # Check against patterns (using glob matching logic)
        import fnmatch
        for p in patterns:
            if fnmatch.fnmatch(str(alias), p):
                resource_files.append((alias, f))
                print(f"Adding {f}")
                break

    # Config file
    config_file = None
    if args.config:
        if args.config.exists():
            config_file = args.config
        elif (args.baseDir / args.config).exists():
            config_file = args.baseDir / args.config

    # Icons
    icon_files = []
    if args.iconsDir and args.iconsDir.exists():
        icon_files = list(args.iconsDir.glob('*'))

    # Generate QRC
    qrc_path = Path('resources.qrc')
    with qrc_path.open('w', encoding='utf-8') as qrc:
        qrc.write('<!DOCTYPE RCC><RCC version="1.0">\n')
        prefix_attr = f" prefix='{args.dirPrefix}'" if args.dirPrefix else ""
        qrc.write(f'\t<qresource{prefix_attr}>\n')
        for alias, path in resource_files:
            # Use forward slashes for alias as required by RCC
            alias_str = str(alias).replace('\\', '/')
            qrc.write(f"\t\t<file alias='{alias_str}'>{path}</file>\n")
        qrc.write('\t</qresource>\n')
        
        qrc.write('\t<qresource>\n')
        stylesheet_path = args.style if args.style.is_absolute() else (args.baseDir / args.style)
        qrc.write(f"\t\t<file alias='stylesheet.qss'>{stylesheet_path}</file>\n")
        for icon in icon_files:
            # Icons are usually expected in an 'icons' directory in the theme
            qrc.write(f"\t\t<file alias='icons/{icon.name}'>{icon}</file>\n")
        if config_file:
            qrc.write(f"\t\t<file alias='config.json'>{config_file}</file>\n")
        qrc.write('\t</qresource>\n')
        qrc.write('</RCC>')

    # Compile
    rcc_bin = get_rcc_bin()
    if not rcc_bin:
        print("Error: rcc not found. Please install Qt development tools.")
        sys.exit(1)

    cmd = [rcc_bin, '-binary', '-o', str(output_path), str(qrc_path)]
    print(f"Executing: {' '.join(cmd)}")
    
    try:
        ret = subprocess.call(cmd)
        if ret == 0:
            qrc_path.unlink()
            print(f"Successfully built {output_path}")
        else:
            print(f"RCC failed with exit code {ret}")
    except Exception as e:
        print(f"Error executing RCC: {e}")

if __name__ == '__main__':
    main()