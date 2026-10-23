from __future__ import annotations

import json
import os
from typing import Iterable, List, Optional

from openai import OpenAI


OPENAI_MODEL = "gpt-4o-mini"



def quality_summary(
    source_texts: Iterable[str],
    translated_texts: Iterable[str],
    source_language: str,
    target_language: str,
    style_guide: Optional[str] = None,
) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is required")
    src_list: List[str] = list(source_texts)
    tgt_list: List[str] = list(translated_texts)
    if len(src_list) != len(tgt_list):
        raise ValueError("source_texts and translated_texts must have the same length")
    client = OpenAI(api_key=api_key)
    payload = {
        "source_language": source_language,
        "target_language": target_language,
        "style_guide": style_guide,
        "pairs": [
            {"source": src, "translation": tgt}
            for src, tgt in zip(src_list, tgt_list)
        ],
    }
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.2,
        messages=[
            {
                "role": "system",
                "content": "You review translations and summarize quality issues concisely, focusing on accuracy, terminology, fluency, omissions, and formatting.",
            },
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
    )
    return response.choices[0].message.content or ""
