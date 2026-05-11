import os
import requests
from pathlib import Path

# All known qBittorrent icon names -> Google Symbol Names
MAPPING = {
    "application-exit.svg": "exit_to_app",
    "application-rss.svg": "rss_feed",
    "application-url.svg": "link",
    "browser-cookies.svg": "cookie",
    "chart-line.svg": "show_chart",
    "checked-completed.svg": "check_circle",
    "configure.svg": "settings",
    "connected.svg": "cloud_done",
    "dialog-warning.svg": "warning",
    "directory.svg": "folder",
    "disconnected.svg": "cloud_off",
    "download.svg": "download",
    "downloading.svg": "downloading",
    "edit-clear.svg": "clear_all",
    "edit-copy.svg": "content_copy",
    "edit-find.svg": "search",
    "edit-rename.svg": "edit",
    "error.svg": "error",
    "fileicon.svg": "description",
    "filter-active.svg": "filter_alt",
    "filter-all.svg": "filter_list",
    "filter-inactive.svg": "filter_alt_off",
    "filter-stalled.svg": "hourglass_empty",
    "firewalled.svg": "security",
    "folder-documents.svg": "folder",
    "folder-new.svg": "create_new_folder",
    "folder-remote.svg": "cloud",
    "force-recheck.svg": "find_replace",
    "go-bottom.svg": "vertical_align_bottom",
    "go-down.svg": "arrow_downward",
    "go-top.svg": "vertical_align_top",
    "go-up.svg": "arrow_upward",
    "hash.svg": "tag",
    "help-about.svg": "info",
    "help-contents.svg": "help",
    "insert-link.svg": "link",
    "ip-blocked.svg": "block",
    "list-add.svg": "add",
    "list-remove.svg": "remove",
    "loading.svg": "sync",
    "mail-inbox.svg": "inbox",
    "name.svg": "title",
    "network-connect.svg": "wifi",
    "network-server.svg": "dns",
    "object-locked.svg": "lock",
    "pause-session.svg": "pause",
    "paused.svg": "pause",
    "peers-add.svg": "person_add",
    "peers-remove.svg": "person_remove",
    "peers.svg": "group",
    "plugins.svg": "extension",
    "preferences-advanced.svg": "tune",
    "preferences-bittorrent.svg": "hub",
    "preferences-desktop.svg": "desktop_windows",
    "preferences-webui.svg": "public",
    "qbittorrent-tray.svg": "bolt",
    "qbittorrent-tray-dark.svg": "bolt",
    "qbittorrent-tray-light.svg": "bolt",
    "qbittorrent_mac.svg": "bolt",
    "queued.svg": "schedule",
    "ratio.svg": "percent",
    "reannounce.svg": "refresh",
    "rss_read_article.svg": "drafts",
    "rss_unread_article.svg": "mail",
    "security-high.svg": "verified_user",
    "security-low.svg": "gpp_maybe",
    "set-location.svg": "location_on",
    "slow.svg": "speed",
    "slow_off.svg": "speed",
    "speedometer.svg": "speed",
    "stalledDL.svg": "file_download_off",
    "stalledUP.svg": "file_upload_off",
    "stopped.svg": "stop",
    "system-log-out.svg": "logout",
    "tags.svg": "label",
    "task-complete.svg": "task_alt",
    "task-reject.svg": "cancel",
    "torrent-creator.svg": "add_box",
    "torrent-magnet.svg": "link",
    "torrent-start-forced.svg": "play_arrow",
    "torrent-start.svg": "play_arrow",
    "torrent-stop.svg": "stop",
    "torrent-pause.svg": "pause",
    "pause.svg": "pause",
    "media-playback-pause.svg": "pause",
    "media-playback-start.svg": "play_arrow",
    "media-playback-stop.svg": "stop",
    "tracker-error.svg": "cloud_off",
    "tracker-warning.svg": "cloud_queue",
    "trackerless.svg": "public_off",
    "trackers.svg": "router",
    "upload.svg": "upload",
    "view-categories.svg": "category",
    "view-preview.svg": "preview",
    "view-refresh.svg": "refresh",
    "view-statistics.svg": "bar_chart",
    "wallet-open.svg": "account_balance_wallet",
    # Additional from other themes
    "media-seek-forward.svg": "fast_forward",
    "network-wired.svg": "lan",
    "office-chart-line.svg": "show_chart",
    "preferences-other.svg": "more_horiz",
    "preferences-system-network.svg": "settings_ethernet",
    "preferences-web-browser-cookies.svg": "cookie",
    "resumed.svg": "play_arrow",
    "rss-config.svg": "rss_feed",
    "seeding.svg": "cloud_upload",
    "services.svg": "miscellaneous_services",
    "tab-close.svg": "close",
    "task-attention.svg": "priority_high",
    "task-ongoing.svg": "pending",
    "text-plain.svg": "description",
    "tools-report-bug.svg": "bug_report",
    "unavailable.svg": "block",
    "uploading.svg": "upload",
    "user-group-delete.svg": "person_remove",
    "user-group-new.svg": "person_add",
    "view-calendar-journal.svg": "event_note",
    "view-filter.svg": "filter_alt",
    "webui.svg": "public",
    "regex.svg": "regular_expression",
    "spinner.svg": "sync",
    "toolbox-divider.svg": "horizontal_rule"
}

BASE_URL = "https://raw.githubusercontent.com/google/material-design-icons/master/symbols/web/{name}/materialsymbolsrounded/{name}_24px.svg"
ICONS_DIR = Path(__file__).parent.parent / "src/material-dark/icons"

def download_icons():
    if not ICONS_DIR.exists():
        ICONS_DIR.mkdir(parents=True)
    
    # Recursively find all icons to delete
    for f in ICONS_DIR.rglob("*.svg"):
        f.unlink()

    for filename, symbol in MAPPING.items():
        url = BASE_URL.format(name=symbol)
        print(f"Hunting {symbol} for {filename}...")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                with open(ICONS_DIR / filename, "w") as f:
                    f.write(response.text)
                print(f"Successfully caught {symbol}!")
            else:
                # Try fallback names if 404
                print(f"Failed to catch {symbol} (Status: {response.status_code})")
        except Exception as e:
            print(f"Error hunting {symbol}: {e}")

if __name__ == "__main__":
    download_icons()
