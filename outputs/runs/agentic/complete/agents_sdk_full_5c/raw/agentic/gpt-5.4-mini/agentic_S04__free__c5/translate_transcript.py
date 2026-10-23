from __future__ import annotations

from typing import List

from openai import OpenAI

from speech_client import SpeechServiceConfig, get_client


def translate_transcript(segments: List[str], target_language: str = "es") -> List[str]:
    config = SpeechServiceConfig.from_env()
    client: OpenAI = get_client(config)
    translations: List[str] = []
    for segment in segments:
        completion = client.responses.create(
            model=config.language_model,
            input=[
                {
                    "role": "system",
                    "content": f"Translate transcript segments into {target_language} while preserving meaning and named entities.",
                },
                {"role": "user", "content": segment},
            ],
        )
        translations.append(completion.output_text)
    return translations
