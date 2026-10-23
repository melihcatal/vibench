import os
from typing import Optional

import requests


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def check_ocr_text_safety(text: str) -> dict:
    if not text.strip():
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "model": OPENAI_MODERATION_MODEL,
        }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
        "model": OPENAI_MODERATION_MODEL,
    }
    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers=headers,
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    if not results:
        return {
            "flagged": False,
            "categories": {},
            "category_scores": {},
            "model": OPENAI_MODERATION_MODEL,
        }
    result = results[0]
    return {
        "flagged": result.get("flagged", False),
        "categories": result.get("categories", {}),
        "category_scores": result.get("category_scores", {}),
        "model": OPENAI_MODERATION_MODEL,
    }


def check_ocr_text_safety_batch(texts: list) -> list:
    if not texts:
        return []
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": texts,
        "model": OPENAI_MODERATION_MODEL,
    }
    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    output = []
    for idx, result in enumerate(results):
        output.append(
            {
                "text": texts[idx] if idx < len(texts) else "",
                "flagged": result.get("flagged", False),
                "categories": result.get("categories", {}),
                "category_scores": result.get("category_scores", {}),
                "model": OPENAI_MODERATION_MODEL,
            }
        )
    return output


def get_safety_summary(safety_result: dict) -> dict:
    flagged = safety_result.get("flagged", False)
    categories = safety_result.get("categories", {})
    scores = safety_result.get("category_scores", {})
    flagged_categories = [cat for cat, is_flagged in categories.items() if is_flagged]
    highest_score_category = ""
    highest_score = 0.0
    for cat, score in scores.items():
        if score > highest_score:
            highest_score = score
            highest_score_category = cat
    return {
        "is_safe": not flagged,
        "flagged_categories": flagged_categories,
        "highest_risk_category": highest_score_category,
        "highest_risk_score": highest_score,
        "model": safety_result.get("model", OPENAI_MODERATION_MODEL),
    }
