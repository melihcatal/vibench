from typing import Iterable, List

from openai import OpenAI

from speech_client import load_speech_config


def live_caption_translate(chunks: Iterable[str], target_language: str = "es") -> List[str]:
    config = load_speech_config("openai", model="gpt-4o-mini")
    client = OpenAI(api_key=config.api_key)
    outputs: List[str] = []
    for chunk in chunks:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": f"Translate live captions to {target_language}."}, {"role": "user", "content": chunk}],
        )
        outputs.append(response.choices[0].message.content or "")
    return outputs
