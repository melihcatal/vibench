from typing import List

from openai import OpenAI

from translation_client import load_config


QUALITY_SUMMARY_MODEL = "gpt-4.1-mini"


def summarize_translation_quality(translation: str, source_text: str, source_language: str, target_language: str) -> str:
    cfg = load_config()
    client = OpenAI(api_key=cfg.api_key) if cfg.api_key else OpenAI()
    prompt = (
        f"Assess translation quality for {source_language} -> {target_language}. "
        "List likely issues concisely: meaning drift, omissions, terminology, grammar, tone.\n\n"
        f"Source:\n{source_text}\n\nTranslation:\n{translation}"
    )
    response = client.responses.create(model=QUALITY_SUMMARY_MODEL, input=prompt)
    return response.output_text
