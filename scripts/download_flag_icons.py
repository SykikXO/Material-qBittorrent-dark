import requests
from pathlib import Path

# Get list of flags from qBittorrent repo
LIST_URL = "https://api.github.com/repos/qbittorrent/qBittorrent/contents/src/icons/flags"
FLAG_SOURCE_URL = "https://hatscripts.github.io/circle-flags/flags/{code}.svg"
FLAGS_DIR = Path(__file__).parent.parent / "src" / "material-dark" / "icons" / "flags"

def download_flags():
    if not FLAGS_DIR.exists():
        FLAGS_DIR.mkdir(parents=True)
    
    print("Listing official flag names...")
    try:
        response = requests.get(LIST_URL)
        if response.status_code == 200:
            official_flags = [item['name'] for item in response.json() if item['name'].endswith('.svg')]
        else:
            print(f"Failed to list flags (Status: {response.status_code})")
            return
    except Exception as e:
        print(f"Error listing flags: {e}")
        return

    print(f"Found {len(official_flags)} flags to hunt.")
    
    for filename in official_flags:
        code = filename.replace('.svg', '')
        # Special cases or remapping if needed
        # circle-flags uses lowercase ISO codes, mostly same as qBittorrent
        url = FLAG_SOURCE_URL.format(code=code)
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(FLAGS_DIR / filename, "w") as f:
                    f.write(response.text)
                print(f"Caught flag: {filename}")
            else:
                # Fallback to official if not found in circle-flags
                print(f"Flag {code} not in circle-flags, trying official...")
                official_raw = f"https://raw.githubusercontent.com/qbittorrent/qBittorrent/master/src/icons/flags/{filename}"
                off_resp = requests.get(official_raw)
                if off_resp.status_code == 200:
                    with open(FLAGS_DIR / filename, "w") as f:
                        f.write(off_resp.text)
                    print(f"Caught official flag: {filename}")
        except Exception as e:
            print(f"Error hunting flag {filename}: {e}")

if __name__ == "__main__":
    download_flags()
