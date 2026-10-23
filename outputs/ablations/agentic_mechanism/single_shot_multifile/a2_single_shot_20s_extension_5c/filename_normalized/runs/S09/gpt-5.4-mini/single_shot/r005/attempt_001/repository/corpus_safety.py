import os
from collections.abc import Sequence

from openai import OpenAI

DEFAULT_MODEL = os.getenv("OPENAI_SAFETY_MODEL", "gpt-4o-mini")


def check_corpus_text_before_embedding(texts: Sequence[str], model: str = DEFAULT_MODEL) -> dict[str, object]:
    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    content = "\n".join(texts)
    response = client.moderations.create(model=model, input=content)
    result = response.results[0]
    return {
        "flagged": bool(result.flagged),
        "categories": dict(getattr(result, "categories", {})),
        "category_scores": dict(getattr(result, "category_scores", {})),
    }
