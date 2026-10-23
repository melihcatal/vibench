from translation_client import get_translation_client

_PROVIDER = "google"


def unsafe_copy_check(text: str) -> dict:
    client = get_translation_client()
    return client.check_unsafe_copy(text)
