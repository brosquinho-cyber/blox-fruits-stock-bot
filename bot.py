import os
import json
import subprocess
import requests

CHANNEL = "https://www.youtube.com/@kenami_main/videos"
THREAD_ID = "1551889614321491978"
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]

STATE_FILE = "state.json"

FRUITS = [
    "Rocket", "Spin", "Blade", "Bomb", "Smoke", "Spike",
    "Flame", "Falcon", "Ice", "Sand", "Dark", "Diamond",
    "Light", "Rubber", "Barrier", "Ghost", "Magma", "Quake",
    "Buddha", "Love", "Spider", "Sound", "Phoenix", "Portal",
    "Rumble", "Pain", "Blizzard", "Gravity", "Mammoth",
    "T-Rex", "Dough", "Shadow", "Venom", "Control",
    "Spirit", "Dragon", "Leopard", "Kitsune", "Yeti"
]

def get_state():
    if not os.path.exists(STATE_FILE):
        return []
    with open(STATE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)

def get_videos():
    command = [
        "yt-dlp",
        "--flat-playlist",
        "--playlist-end", "10",
        "--print", "%(id)s|%(title)s",
        CHANNEL
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    videos = []

    for line in result.stdout.splitlines():
        if "|" in line:
            video_id, title = line.split("|", 1)
            videos.append({
                "id": video_id,
                "title": title
            })

    return videos

def find_fruits(title):
    found = []

    title_lower = title.lower()

    for fruit in FRUITS:
        if fruit.lower() in title_lower:
            found.append(fruit)

    return found

def send_discord(message):
    url = f"https://discord.com/api/v10/channels/{THREAD_ID}/messages"

    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json"
    }

    data = {
        "content": message
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    if response.status_code not in (200, 201):
        print("Erro Discord:", response.status_code, response.text)

def main():
    state = get_state()
    videos = get_videos()

    for video in reversed(videos):
        video_id = video["id"]

        if video_id in state:
            continue

        fruits = find_fruits(video["title"])

        if fruits:
            for fruit in fruits:
                send_discord(fruit)

        state.append(video_id)

    state = state[-50:]
    save_state(state)

if __name__ == "__main__":
    main()
