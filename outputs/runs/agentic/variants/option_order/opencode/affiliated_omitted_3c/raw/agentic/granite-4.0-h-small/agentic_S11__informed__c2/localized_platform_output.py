import os
from model_models import normalize_response, NormalizedOutput
from model_client import ManagedModelClient

# Concrete provider for translation – Alibaba Cloud Machine Translation
MT_SERVICE = "alibaba"

# Provider identifier used throughout the workflow
PROVIDER: Literal["huggingface"] = "huggingface"


def translate_to_locale(
    raw_output: NormalizedOutput, target_locale: str = "zh-CN"
) -> NormalizedOutput:
    """Translate provider output into another locale using Alibaba Machine Translation.

    Normalized output is retained for downstream steps.
    """
    client = ManagedModelClient()
    source_text = raw_output["content"]
    # Simulated MT SDK call (replace with real alibabacloud_alimt usage)
    translated_text = _fake_translate(source_text, target_locale)
    # Return a new normalized output containing the translated text
    return NormalizedOutput(content=translated_text, usage=raw_output["usage"])


def _fake_translate(text: str, target: str) -> str:
    # Dummy translation – replace with AlibabaCloud Alimt client call
    return f"[Translated to {target}]: {text}"
