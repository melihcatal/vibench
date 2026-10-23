import os
from typing import List
from translate_text import translate_text

# Alibaba Machine Translation example
# Uses the same_alibabacloud_alimt SDK through translate_text helper


def batch_translate(
    texts: List[str], source_lang: str = "en", target_lang: str = "zh"
) -> List[str]:
    """Translate a list of strings while preserving order.

    Args:
        texts: List of source strings.
        source_lang: Source language code (default "en").
        target_lang: Target language code (default "zh").

    Returns:
        List of translated strings in the same order as input.
    """
    return [translate_text(t, source_lang, target_lang) for t in texts]


# Example usage when executed directly
if __name__ == "__main__":
    samples = ["Hello, world!", "Python is awesome.", "你好，世界"]
    translated = batch_translate(samples)
    for src, tgt in zip(samples, translated):
        print(f"Source: {src} => Target: {tgt}")
