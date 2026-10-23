from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Mapping, Optional

from google.cloud import language_v1

from security_models import DecryptPayloadResponse, normalize_plaintext, response_from_mapping


@dataclass(frozen=True)
class PayloadSafetyFinding:
    category: str
    severity: str
    score: float = 0.0
    snippet: str = ""


@dataclass(frozen=True)
class PayloadSafetyRequest:
    plaintext: str = ""
    language_hint: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> "PayloadSafetyRequest":
        return PayloadSafetyRequest(
            plaintext=normalize_plaintext(self.plaintext),
            language_hint=(self.language_hint or "").strip(),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class PayloadSafetyResponse:
    ok: bool = False
    unsafe: bool = False
    provider: str = "google-cloud-language"
    findings: List[PayloadSafetyFinding] = field(default_factory=list)
    analyzed_text: str = ""
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> "PayloadSafetyResponse":
        return PayloadSafetyResponse(
            ok=bool(self.ok),
            unsafe=bool(self.unsafe),
            provider=self.provider or "google-cloud-language",
            findings=list(self.findings),
            analyzed_text=normalize_plaintext(self.analyzed_text),
            metadata=dict(self.metadata),
        )


class PayloadSafetyChecker:
    def __init__(self, client: Optional[language_v1.LanguageServiceClient] = None) -> None:
        self._client = client or language_v1.LanguageServiceClient()

    def _suspicious_rules(self, text: str) -> Iterable[PayloadSafetyFinding]:
        lowered = text.lower()
        rules = (
            ("secret", "high", "contains secret-like material"),
            ("password", "high", "contains password-like material"),
            ("api key", "high", "contains api key-like material"),
            ("token", "medium", "contains token-like material"),
            ("ssn", "high", "contains ssn-like material"),
            ("credit card", "high", "contains payment card material"),
            ("malware", "high", "contains malware references"),
            ("exploit", "high", "contains exploit references"),
        )
        for needle, severity, category in rules:
            if needle in lowered:
                yield PayloadSafetyFinding(category=category, severity=severity, score=0.9, snippet=needle)

    def analyze(self, request: PayloadSafetyRequest | Mapping[str, Any]) -> PayloadSafetyResponse:
        if isinstance(request, Mapping):
            request = PayloadSafetyRequest(**dict(request))
        req = request.normalized()
        text = req.plaintext
        findings = list(self._suspicious_rules(text))
        if text:
            document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)
            _ = self._client.analyze_sentiment(request={"document": document})
        unsafe = any(f.severity == "high" for f in findings)
        return PayloadSafetyResponse(
            ok=True,
            unsafe=unsafe,
            provider="google-cloud-language",
            findings=findings,
            analyzed_text=text,
            metadata=dict(req.metadata),
        ).normalized()


def check_payload_safety(payload: DecryptPayloadResponse | Mapping[str, Any] | str) -> PayloadSafetyResponse:
    if isinstance(payload, DecryptPayloadResponse):
        text = payload.plaintext
        metadata = dict(payload.metadata)
    elif isinstance(payload, Mapping):
        text = str(payload.get("plaintext", ""))
        metadata = dict(payload)
    else:
        text = str(payload)
        metadata = {}
    return PayloadSafetyChecker().analyze(PayloadSafetyRequest(plaintext=text, metadata=metadata))


def is_safe_payload(payload: DecryptPayloadResponse | Mapping[str, Any] | str) -> bool:
    return not check_payload_safety(payload).unsafe
