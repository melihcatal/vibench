from typing import List, Dict, Any


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_ssml(ssml: str) -> str:
    return ssml.strip()


VoiceInfo = Dict[str, Any]
