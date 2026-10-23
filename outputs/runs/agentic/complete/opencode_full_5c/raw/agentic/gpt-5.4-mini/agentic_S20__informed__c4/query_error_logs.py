from observability_client import fetch_recent


def main() -> list[dict]:
    return fetch_recent(severity='ERROR', filters={'service': 'billing'}, minutes=120).records
