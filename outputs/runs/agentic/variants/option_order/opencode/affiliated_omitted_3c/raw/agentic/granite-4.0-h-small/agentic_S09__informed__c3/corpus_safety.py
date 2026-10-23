import os
import json
from typing import List

# Provider identified by SDK import and model identifier


class CorpusSafety:
    """Checks corpus text before embedding to ensure safety and quality."""

    @staticmethod
    def is_safe(text: str) -> bool:
        """Simple heuristic check; replace with real moderation API in production."""
        lower = text.lower()
        disallowed = ["hate", "violence", "sexual", "offensive"]
        return not any(word in lower for word in disallowed)

    @classmethod
    def filter_corpus(cls, corpus: List[str]) -> List[str]:
        """Returns only safe texts from the input corpus."""
        return [txt for txt in corpus if cls.is_safe(txt)]

    @staticmethod
    def warn_unsafe(text: str) -> None:
        print(f"WARNING: Unsafe content detected and omitted: {text[:30]}...")
