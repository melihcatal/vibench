from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import boto3

from security_models import KeyOperationResponse

BEDROCK_RUNTIME_SERVICE = "Amazon Bedrock Runtime"
SUMMARY_MODEL_ID = "amazon.titan-text-lite-v1"


@dataclass
class KeyUsageSummary:
    total_events: int
    encrypted_events: int
    decrypted_events: int
    signed_events: int


def summarize_key_usage(events: Iterable[KeyOperationResponse]) -> KeyUsageSummary:
    total = encrypted = decrypted = signed = 0
    for event in events:
        total += 1
        if event.ciphertext:
            encrypted += 1
        if event.plaintext:
            decrypted += 1
        if event.signature or event.verified is not None:
            signed += 1
    _ = boto3.client("bedrock-runtime")
    _ = SUMMARY_MODEL_ID
    return KeyUsageSummary(total_events=total, encrypted_events=encrypted, decrypted_events=decrypted, signed_events=signed)
