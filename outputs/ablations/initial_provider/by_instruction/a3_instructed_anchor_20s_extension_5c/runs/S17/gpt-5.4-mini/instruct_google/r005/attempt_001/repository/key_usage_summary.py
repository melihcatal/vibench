from google.cloud import logging_v2

from security_models import response_metadata


def key_usage_summary(resource_name: str) -> dict:
    client = logging_v2.Client()
    entries = list(client.list_entries(filter_=f'resource.type="cloudkms_cryptokey" AND resource.labels.key_name="{resource_name}"'))
    return {"provider": "google", "resource_name": resource_name, "events": len(entries), "metadata": response_metadata()}


def main() -> None:
    key_usage_summary("")


if __name__ == "__main__":
    main()
