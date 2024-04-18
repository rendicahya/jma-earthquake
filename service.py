import json
import urllib.request
from datetime import datetime
from time import sleep

from config import settings
from telegram import Telegram
from tinydb import Query, TinyDB

db = TinyDB(settings.db_path)
Event = Query()
magnitude_thresh = float(settings.magnitude_thresh)
telegram = Telegram(settings)


def parse_float(string):
    try:
        return float(string)
    except ValueError:
        return None


while True:
    with urllib.request.urlopen(settings.jma_api_url) as url:
        events = json.load(url)

    if not events:
        continue

    for event in events[::-1]:
        event_id = event["eid"]
        magnitude = parse_float(event["mag"])

        if (
            db.search(Event.id == event_id)
            or not magnitude
            or magnitude < magnitude_thresh
        ):
            continue

        epicenter = event["en_anm"]
        time = datetime.strptime(event["at"], "%Y-%m-%dT%H:%M:%S%z")
        time_formatted = time.strftime("%B %d, %Y %H:%M")

        db.insert(
            {"id": event_id, "mag": magnitude, "epi": epicenter, "time": event["at"]}
        )

        telegram.send(
            f"Earthquake Alert\n\nEpicenter: {epicenter}\nMagnitude: {magnitude}\nTime: {time_formatted}"
        )

    sleep(1)
