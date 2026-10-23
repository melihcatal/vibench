import asyncio
from typing import List
from translate_text import translate_text

PROVIDER_NAME = "deepl"


async def batch_translate(
    texts: List[str], target_lang: str, source_lang: str = "auto"
) -> List[str]:
    """Translate a list of strings while preserving order.",
    Uses asynchronous concurrency to improve throughput while maintaining order."""
    # Prepare individual tasks and keep their original indices
    tasks = {
        i: translate_text(text, target_lang, source_lang)
        for i, text in enumerate(texts)
    }
    # Execute concurrently and gather results in original order
    results = await asyncio.gather(*tasks.values())
    # Reorder according to the original indices
    ordered = [None] * len(results)
    for i, result in tasks.items():
        ordered[i] = result
    return ordered
