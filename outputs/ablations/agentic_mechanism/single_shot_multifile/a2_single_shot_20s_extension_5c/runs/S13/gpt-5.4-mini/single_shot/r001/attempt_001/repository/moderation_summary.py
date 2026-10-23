from typing import Any, Dict, Iterable, List
from openai import OpenAI
from safety_client import get_openai_client

SUMMARY_MODEL = "gpt-4.1-mini"


def moderation_summary(decisions: Iterable[Dict[str, Any]], *, model: str | None = None) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    chosen_model = model or SUMMARY_MODEL
    lines: List[str] = []
    for item in decisions:
        lines.append(f"index={item.get('index')} flagged={item.get('flagged')} categories={item.get('categories')}")
    prompt = "Summarize moderation decisions for an operations reviewer.\n" + "\n".join(lines)
    response = client.responses.create(model=chosen_model, input=prompt)
    return {"summary": response.output_text, "model": chosen_model}


if __name__ == "__main__":
    raise SystemExit(0)
