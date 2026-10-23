from typing import Iterable, List
from google.cloud import secretmanager

_UNSAFE_MARKERS = ("password", "secret", "token", "key", "drop table", "rm -rf", "<script>")


def secret_label_safety(labels: Iterable[str], notes: str) -> bool:
    secretmanager.SecretManagerServiceClient()
    combined = " ".join(list(labels) + [notes]).lower()
    return not any(marker in combined for marker in _UNSAFE_MARKERS)
