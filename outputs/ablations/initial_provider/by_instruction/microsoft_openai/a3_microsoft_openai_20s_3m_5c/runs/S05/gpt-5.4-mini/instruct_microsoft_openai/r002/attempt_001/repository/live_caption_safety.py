from typing import Iterable, List

from openai import OpenAI

from speech_client import load_speech_config


def live_caption_safety(chunks: Iterable[str]) -> List[str]:
    config = load_speech_config("openai", model="gpt-4o-mini")
    client = OpenAI(api_key=config.api_key)
    findings: List[str] = []
    for chunk in chunks:
        response = client.moderations.create(model="omni-moderation-latest", input=chunk)
        flagged = response.results[0].flagged
        findings.append("unsafe" if flagged else "safe")
    return findings
