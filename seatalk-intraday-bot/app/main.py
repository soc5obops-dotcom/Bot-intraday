import time
from datetime import datetime
from zoneinfo import ZoneInfo

from config import load_settings
from sheets_client import SheetsClient
from state_store import StateStore


def flatten_values(values: list[list[str]]) -> str:
    parts = []
    for row in values:
        for cell in row:
            parts.append(str(cell).strip())
    return " | ".join(parts)


def now_str(tz_name: str) -> str:
    return datetime.now(ZoneInfo(tz_name)).strftime("%Y-%m-%d %H:%M:%S %Z")


def run_check(client: SheetsClient, store: StateStore, settings) -> None:
    full_range = f"{settings.tab_name}!{settings.watch_range}"
    values = client.read_range(settings.sheet_id, full_range)
    current_key = flatten_values(values)
    previous_key = store.load_last_key()

    print("========================================")
    print(f"Check time: {now_str(settings.tz)}")
    print(f"Range: {full_range}")
    print(f"Current values: {values}")
    print(f"Current key: {current_key}")
    print(f"Previous key: {previous_key}")

    if not current_key:
        print("Result: watched range is blank; nothing to save.")
        return

    if previous_key is None:
        print("Result: first run detected; saving current key.")
        store.save_last_key(current_key)
        return

    if current_key != previous_key:
        print("Result: CHANGED")
        store.save_last_key(current_key)
    else:
        print("Result: UNCHANGED")


def main():
    settings = load_settings()
    client = SheetsClient(settings.google_service_account_info)
    store = StateStore(settings.state_file)

    print("Bot service started.")
    print(f"Polling every {settings.poll_interval_seconds} seconds.")
    print(f"Timezone: {settings.tz}")

    while True:
        try:
            run_check(client, store, settings)
        except Exception as exc:
            print("Result: ERROR")
            print(f"Error details: {exc}")

        time.sleep(settings.poll_interval_seconds)


if __name__ == "__main__":
    main()