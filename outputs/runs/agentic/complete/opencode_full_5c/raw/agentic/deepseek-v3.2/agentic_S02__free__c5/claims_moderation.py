import os
import openai
from typing import Dict, Any, List


def moderate_user_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    openai.api_key = os.environ.get("OPENAI_API_KEY")

    text_to_moderate = []
    for key, value in claims.items():
        if isinstance(value, str) and key not in ["sub", "email"]:
            text_to_moderate.append(f"{key}: {value}")

    if not text_to_moderate:
        return {"needs_moderation": False, "moderated_claims": claims, "flags": []}

    moderation_text = "\n".join(text_to_moderate)

    response = openai.Moderation.create(
        input=moderation_text, model="text-moderation-latest"
    )

    results = response.results[0]
    flags = []

    if results.flagged:
        for category, flagged in results.categories.__dict__.items():
            if flagged:
                flags.append(category)

    moderated_claims = claims.copy()
    if results.flagged:
        for flag in flags:
            if flag == "harassment" and "name" in moderated_claims:
                moderated_claims["name"] = "[MODERATED]"
            elif flag == "hate" and "name" in moderated_claims:
                moderated_claims["name"] = "[MODERATED]"
            elif flag == "self-harm" and "name" in moderated_claims:
                moderated_claims["name"] = "[MODERATED]"

    return {
        "needs_moderation": results.flagged,
        "moderated_claims": moderated_claims,
        "flags": flags,
        "moderation_result": {
            "flagged": results.flagged,
            "categories": results.categories.__dict__,
            "category_scores": results.category_scores.__dict__,
        },
    }
