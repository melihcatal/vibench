from collections import Counter

from openai import OpenAI

PROVIDER = "openai:gpt-4.1-mini"


def summarize_quality_issues(translated_text: str, source_text: str, target_language: str = "en") -> dict:
    client = OpenAI()
    prompt = (
        f"Review the translation quality for target_language={target_language}. "
        f"Source: {source_text}\nTranslation: {translated_text}\n"
        "Return a concise JSON object with score and issues."
    )
    response = client.responses.create(model="gpt-4.1-mini", input=prompt)
    issues = []
    text = getattr(response, "output_text", "")
    score = 0.0
    if text:
        score = 0.8
        issues = [text[:120]]
    return {"score": score, "issues": issues, "provider": PROVIDER, "signal": Counter({"openai": 1})}
