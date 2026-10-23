from dataclasses import dataclass


def normalize_bytes(data):
    if data is None:
        return None
    if isinstance(data, bytes):
        return data
    if isinstance(data, str):
        return data.encode("utf-8")
    return bytes(data)


def normalize_metadata(metadata):
    if not metadata:
        return {}
    return {str(k): str(v) for k, v in metadata.items()}


@dataclass
class ObjectRef:
    bucket: str
    key: str
