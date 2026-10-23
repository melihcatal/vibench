from observability_client import fetch_recent


def main() -> list[dict]:
    return fetch_recent(filters={'component': 'api'}, minutes=30).records
