import google.generativeai as genai
from typing import Dict, Any, List
from safety_client import get_api_key

THRESHOLDS = {
    "hate": 0.5,
    "harassment": 0.8,
    "self_harm": 0.7,
    "sexual": 0.7,
    "violence": 0.7,
    "toxicity": 0.5,
}


def safety_threshold(decision: Dict[str, Any]) -> bool:
    categories_str = ", ".join(
        [f"{c['category']}:{c['score']:.2f}" for c in decision["categories"]]
    )
    prompt = f"""Moderation categories and scores: {categories_str}

Block thresholds: {THRESHOLDS}

Should this text be allowed? Respond ONLY with 'YES' or 'NO'."""
    api_key = get_api_key("GOOGLE_GENAI_API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    result = response.text.strip().upper()
    return result == "YES"
