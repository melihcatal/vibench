from datetime import datetime, timedelta, timezone

from observability_client import recent_events


def main() -> None:
    recent_events(limit=50)


if __name__ == "__main__":
    main()
