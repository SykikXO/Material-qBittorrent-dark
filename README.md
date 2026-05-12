# Material qBittorrent
A premium dark theme for qBittorrent featuring Material Design Symbols and Google Sans typography. Optimized for high contrast and modern aesthetics.

<h1 align="center">
  <img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-37-24.avif" alt="Material qBittorrent Preview" width="100%"/>
</h1>

## Screenshots

<table>
  <tr>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-37-24.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-38-07.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-39-21.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-40-00.avif" width="100%"/></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-40-32.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-52-16.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-52-46.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-53-24.avif" width="100%"/></td>
  </tr>
  <tr>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-53-48.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-54-26.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-55-24.avif" width="100%"/></td>
    <td><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-56-09.avif" width="100%"/></td>
  </tr>
  <tr>
    <td colspan="4" align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/2026-05-12_05-56-29.avif" width="100%"/></td>
  </tr>
</table>

## Quick Start
1. **Download**: Grab a pre-built theme from the [themes/](themes/) folder (e.g., `Material-Dark-Purple.qbtheme`).
2. **Apply**: In qBittorrent, go to *Tools -> Options -> Behavior*.
3. **Configure**: Check *Use custom UI Theme* and browse to your downloaded file.
4. **Restart**: Restart qBittorrent to apply the changes.

## Installer (Linux)
The included installer script makes it easy to switch between color schemes and automatically updates your qBittorrent configuration.

**One-liner command:**
```bash
curl -sL https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/scripts/install.sh | bash
```

**Local execution:**
```bash
bash scripts/install.sh
```
Follow the interactive prompts to select your favorite color scheme.

## Typography
This theme uses premium typography for a professional look:
- **Google Sans**: Used for all UI text elements for maximum legibility.
- **Material Symbols**: Modern, rounded iconography for a cohesive interface.

*Fonts are bundled within the theme file and do not need to be installed on your system.*

## Build System
If you want to create your own color variations, you can use the "Caveman" build system.

### Prerequisites
- Python 3
- Qt Resource Compiler (`rcc`)

### Compiling
1. Edit `src/material-dark/variables.json` or choose a scheme from `colors/`.
2. Run the compilation script:
```bash
bash scripts/compile.sh
```
The resulting `Material-Dark.qbtheme` will be generated in the project root.




## AI Disclosure
This repository was developed and maintained with the assistance of AI tools.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
