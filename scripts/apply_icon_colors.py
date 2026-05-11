import os
from pathlib import Path

# Mapping of filenames (without extension) to their theme variable
ICON_MAPPING = {
    # Success (Green)
    "torrent-start": "{{SUCCESS}}",
    "torrent-start-forced": "{{SUCCESS}}",
    "media-playback-start": "{{SUCCESS}}",
    "resumed": "{{SUCCESS}}",
    "task-complete": "{{SUCCESS}}",
    "checked-completed": "{{SUCCESS}}",
    "seeding": "{{SUCCESS}}",
    
    # Error (Red)
    "torrent-stop": "{{ERROR}}",
    "stopped": "{{ERROR}}",
    "media-playback-stop": "{{ERROR}}",
    "list-remove": "{{ERROR}}",
    "user-group-delete": "{{ERROR}}",
    "error": "{{ERROR}}",
    "tracker-error": "{{ERROR}}",
    
    # Warning (Yellow)
    "torrent-pause": "{{WARNING}}",
    "pause": "{{WARNING}}",
    "paused": "{{WARNING}}",
    "media-playback-pause": "{{WARNING}}",
    "pause-session": "{{WARNING}}",
    "dialog-warning": "{{WARNING}}",
    "tracker-warning": "{{WARNING}}",
    "stalledDL": "{{WARNING}}",
    "stalledUP": "{{WARNING}}",
    
    # Info / Tertiary / Other
    "downloading": "{{ACCENT}}",
    "uploading": "{{TERTIARY}}",
    "queued": "{{TEXT_SECONDARY}}",
    "force-recheck": "{{INFO}}",
    "reannounce": "{{INFO}}",
    "torrent-magnet": "{{INFO}}",
}

ICON_DIR = Path(__file__).parent.parent / "src/material-dark/icons"

def update_icons():
    # Recursively find all icons in ICON_DIR
    all_icons = {f.name: f for f in ICON_DIR.rglob('*.svg')}
    
    for name, var in ICON_MAPPING.items():
        filename = f"{name}.svg"
        if filename not in all_icons:
            print(f"Skipping {filename} (not found in {ICON_DIR})")
            continue
            
        file_path = all_icons[filename]
        content = file_path.read_text(encoding='utf-8')
        
        # Add or update fill attribute on the SVG tag or Path
        if 'fill=' in content:
            # Replace existing fills (simplified)
            import re
            content = re.sub(r'fill="[^"]+"', f'fill="{var}"', content)
        else:
            # Add fill to the svg tag if not present
            content = content.replace('<svg ', f'<svg fill="{var}" ')
            
        file_path.write_text(content, encoding='utf-8')
        print(f"Updated {name}.svg with {var}")

if __name__ == "__main__":
    update_icons()
