from dataclasses import dataclass
import base64
import json


@dataclass
class SecretFetchRequest:
    secret_id: str
    version_stage: str = 'AWSCURRENT'


@dataclass
class SecretFetchResult:
    secret_id: str
    version_id: str | None
    value: str

    def as_text(self):
        return self.value


def normalize_secret_payload(value):
    if value is None:
        return ''
    if isinstance(value, bytes):
        try:
            return value.decode('utf-8')
        except UnicodeDecodeError:
            return base64.b64encode(value).decode('ascii')
    if isinstance(value, (dict, list)):
        return json.dumps(value)
    return str(value)
