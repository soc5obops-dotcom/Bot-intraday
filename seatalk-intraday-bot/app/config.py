import json
import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    google_service_account_info: dict
    sheet_id: str
    tab_name: str
    watch_range: str
    tz: str
    state_file: str
    poll_interval_seconds: int


def load_settings() -> Settings:
    raw_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
    if not raw_json:
        raise ValueError("Missing GOOGLE_SERVICE_ACCOUNT_JSON in environment.")

    try:
        service_account_info = json.loads(raw_json)
    except json.JSONDecodeError as exc:
        raise ValueError("Invalid GOOGLE_SERVICE_ACCOUNT_JSON format.") from exc

    sheet_id = os.getenv("SHEET_ID", "").strip()
    tab_name = os.getenv("TAB_NAME", "").strip()
    watch_range = os.getenv("WATCH_RANGE", "").strip()
    tz = os.getenv("TZ", "Asia/Manila").strip()
    state_file = os.getenv("STATE_FILE", "/app/data/state.json").strip()

    poll_interval_raw = os.getenv("POLL_INTERVAL_SECONDS", "3600").strip()
    try:
        poll_interval_seconds = int(poll_interval_raw)
    except ValueError as exc:
        raise ValueError("POLL_INTERVAL_SECONDS must be an integer.") from exc

    if poll_interval_seconds <= 0:
        raise ValueError("POLL_INTERVAL_SECONDS must be greater than 0.")

    if not sheet_id:
        raise ValueError("Missing SHEET_ID.")
    if not tab_name:
        raise ValueError("Missing TAB_NAME.")
    if not watch_range:
        raise ValueError("Missing WATCH_RANGE.")

    return Settings(
        google_service_account_info=service_account_info,
        sheet_id=sheet_id,
        tab_name=tab_name,
        watch_range=watch_range,
        tz=tz,
        state_file=state_file,
        poll_interval_seconds=poll_interval_seconds,
    )