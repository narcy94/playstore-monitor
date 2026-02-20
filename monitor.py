import requests
import re
import json
import os

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


def get_playstore_version(package):
    url = f"https://play.google.com/store/apps/details?id={package}&hl=en&gl=us"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code != 200:
        return None

    match = re.search(r'"softwareVersion":"(.*?)"', r.text)
    if match:
        return match.group(1)

    return None


def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)


def load_versions():
    if not os.path.exists(VERSION_FILE):
        return {}
    with open(VERSION_FILE, "r") as f:
        return json.load(f)


def save_versions(data):
    with open(VERSION_FILE, "w") as f:
        json.dump(data, f)


def main():
    saved_versions = load_versions()

    for app in APPS:
        current_version = get_playstore_version(app)
        if not current_version:
            continue

        old_version = saved_versions.get(app)

        if old_version is None:
            saved_versions[app] = current_version
            continue

        if current_version != old_version:
            message = (
                f"🚀 Nueva versión detectada\n\n"
                f"App: {app}\n"
                f"Versión anterior: {old_version}\n"
                f"Nueva versión: {current_version}\n"
                f"https://play.google.com/store/apps/details?id={app}"
            )
            send_telegram(message)
            saved_versions[app] = current_version

    save_versions(saved_versions)


if __name__ == "__main__":
    main()
