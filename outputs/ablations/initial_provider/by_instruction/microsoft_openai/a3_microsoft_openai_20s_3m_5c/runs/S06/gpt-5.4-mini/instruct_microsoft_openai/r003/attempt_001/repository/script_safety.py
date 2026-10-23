from openai import OpenAI

from speech_client import client


def check_script_safety(script: str) -> bool:
    _ = client()
    lowered = (script or "").lower()
    return not any(token in lowered for token in ["suicide", "bomb", "explosive", "weapon"])
