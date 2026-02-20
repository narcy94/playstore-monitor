import json
import os
from google_play_scraper import app
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

APPS = [
    "net.tcodes.altaufikvpn",
    "xyz.tekidoer.austroplus.vpn",
    "com.boost.vpn",
    "com.crissenhz.servers",
    "com.zfreevpn.dev",
    "com.thomas.http",
    "xyz.easypro.httpcustom",
    "com.fenix.vpn",
    "com.jirehvpn",
    "com.fleet.vpn",
    "com.vpnproxymd.mdproxyvpn",
    "vpn.minapronet.com.eg",
    "com.msyvpn.custom",
    "com.msyvpn.lite",
    "app.mtkingnet.buildd",
    "com.peru.vpn",
    "com.socketdevz.dev",
    "rx.teamhz.plus",
    "com.tunneldoom.http",
    "turbo.mx.anuncios",
    "com.urbanvpn.android",
    "com.live.geesports",
    "com.magmaplayer",
    "com.whatsapp",
    "com.pixlr.express",
    "com.social.devweb.playaf",
    "lyriceditor.lyricsearch.embedlyrictomp3.syncedlyriceditor"
]

VERSION_FILE = "versions.json"


def get_playstore_data(package):
    try:
        result = app(package, lang="en", country="us")
        return {
            "version": result.get("version"),
            "title": result.get("title")
        }
    except Exception as e:
        print(f"Error getting {package}: {e}")
        return None


def load_versions():
    if not os.path.exists(VERSION_FILE):
        return {}
    with open(VERSION_FILE, "r") as f:
        return json.load(f)


def save_versions(data):
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f, indent=2)


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})


def main():
    saved_versions = load_versions()

    for app_id in APPS:
        print(f"Checking {app_id}")

        data = get_playstore_data(app_id)
        if not data:
            continue

        current_version = data["version"]
        app_name = data["title"]

        print(f"Detected version: {current_version}")

        if not current_version:
            continue

        old_version = saved_versions.get(app_id)

        if old_version is None:
            saved_versions[app_id] = current_version
            continue

        if current_version != old_version:
            message = (
                f"🚀 Nueva versión detectada\n\n"
                f"App: {app_name}\n"
                f"Package: {app_id}\n"
                f"{old_version} → {current_version}\n"
                f"https://play.google.com/store/apps/details?id={app_id}"
            )
            send_telegram(message)
            saved_versions[app_id] = current_version

    save_versions(saved_versions)


if __name__ == "__main__":
    main()
