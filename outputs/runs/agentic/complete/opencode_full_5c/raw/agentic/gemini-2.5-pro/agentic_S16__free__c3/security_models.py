from dataclasses import dataclass
import json


@dataclass
class SecretPayload:
    raw: bytes

    def as_string(self) -> str:
        return self.raw.decode("UTF-8")

    def as_json(self) -> dict:
        return json.loads(self.as_string())


@dataclass
class UnsafeTextAnalysis:
    is_unsafe: bool
    reasons: list[str]
