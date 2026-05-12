import requests
from pathlib import Path

FONTS_DIR = Path(__file__).parent.parent / "src" / "material-dark" / "fonts"

# Material Symbols from Google Fonts
MATERIAL_SYMBOLS = {
    "MaterialSymbolsRounded-Regular.ttf": (
        "https://raw.githubusercontent.com/google/material-design-icons/master/"
        "variablefont/MaterialSymbolsRounded%5BFILL%2CGRAD%2Copsz%2Cwght%5D.ttf"
    ),
    "MaterialSymbolsOutlined-Regular.ttf": (
        "https://raw.githubusercontent.com/google/material-design-icons/master/"
        "variablefont/MaterialSymbolsOutlined%5BFILL%2CGRAD%2Copsz%2Cwght%5D.ttf"
    ),
    "MaterialSymbolsSharp-Regular.ttf": (
        "https://raw.githubusercontent.com/google/material-design-icons/master/"
        "variablefont/MaterialSymbolsSharp%5BFILL%2CGRAD%2Copsz%2Cwght%5D.ttf"
    ),
}

# Google Sans — proprietary, not publicly downloadable.
# Users can obtain it separately and place the TTF files here:
#   GoogleSans-Regular.ttf
#   GoogleSans-Medium.ttf
#   GoogleSans-Bold.ttf
# Or remove "Google Sans" from the font stack in variables.json to fall back to Inter/Roboto.


def download_fonts():
    FONTS_DIR.mkdir(parents=True, exist_ok=True)

    for filename, url in MATERIAL_SYMBOLS.items():
        dest = FONTS_DIR / filename
        if dest.exists():
            print(f"Skipping {filename} (already exists)")
            continue
        print(f"Downloading {filename}...")
        try:
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            dest.write_bytes(resp.content)
            print(f"  Saved {dest}")
        except Exception as e:
            print(f"  Failed: {e}")

    print()
    print("Material Symbols downloaded.")
    print()
    print("Google Sans is proprietary — not downloaded automatically.")
    print("To use it, place GoogleSans-Regular.ttf, GoogleSans-Medium.ttf,")
    print("and GoogleSans-Bold.ttf in:", FONTS_DIR)
    print("Or remove 'Google Sans' from FONT_FAMILY in src/material-dark/variables.json")


if __name__ == "__main__":
    download_fonts()
