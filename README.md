# Material qBittorrent
A premium dark theme for qBittorrent featuring Material Design Symbols and Google Sans typography. Optimized for high contrast and modern aesthetics.

<p align="center">
  <img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/icon-banner.avif" alt="Material Icons & Typography" width="100%"/>
</p>

## Screenshots

<p align="center">
  <img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/installer-script.avif" width="75%"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/add-torrent-dialog.avif" width="75%"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/torrent-content-selection.avif" width="75%"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/settings.avif" width="75%"/>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/speed-graph.avif" width="75%"/>
</p>

## Color Schemes

<table>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-purple.avif" width="100%"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-blue.avif" width="100%"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-catppuccin.avif" width="100%"/></td>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-dracula.avif" width="100%"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-green.avif" width="100%"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-nord.avif" width="100%"/></td>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-orange.avif" width="100%"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-red.avif" width="100%"/></td>
    <td align="center"><img src="https://raw.githubusercontent.com/SykikXO/Material-qBittorrent-dark/main/previews/theme-rosepine.avif" width="100%"/></td>
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
- `requests` library (`pip install requests`)
- Qt Resource Compiler (`rcc`)

### Fonts
Fonts are not stored in the repository. They are downloaded automatically by
`scripts/download_fonts.py` when you run the build (or manually):
```bash
python3 scripts/download_fonts.py
```
- **Material Symbols** (Apache 2.0) — downloaded from Google's GitHub.
- **Google Sans** (proprietary) — not publicly downloadable. Place the TTF files
  manually in `src/material-dark/fonts/`, or remove `"Google Sans"` from
  `FONT_FAMILY` in `variables.json` to use the fallback (Inter/Roboto).

### Compiling
1. Edit `src/material-dark/variables.json` or choose a scheme from `colors/`.
2. Run the compilation script (this also downloads fonts if missing):
```bash
bash scripts/compile.sh
```
The resulting `Material-Dark.qbtheme` will be generated in the project root.




## AI Disclosure
This repository was developed and maintained with the assistance of AI tools.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
