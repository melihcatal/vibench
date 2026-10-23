from typing import Dict

import google.generativeai as genai

from safety_client import configure_client, generative_model
from safety_models import ModerationDecision, ModerationRequest, normalize_categories, normalize_text

MODERATION_PROMPT = """You are a text safety moderation classifier. Evaluate the text for policy-violating or unsafe content.
Return JSON with keys: allow (boolean), categories (object of numeric scores 0.0-1.0), rationale (short string).
Categories include: harassment, hate, self_harm, sexual, violence, illegal, spam.
Text: {text}"""


def moderate_text(request: ModerationRequest) -> ModerationDecision:
    configure_client()
    prompt = MODERATION_PROMPT.format(text=normalize_text(request.text))
    response = generative_model().generate_content(prompt)
    raw = getattr(response, "text", "") or ""
    parsed = genai.types.GenerationConfig()
    categories: Dict[str, float] = {}
    allow = True
    rationale = raw[:500]
    try:
        import json
        data = json.loads(raw)
        allow = bool(data.get("allow", True))
        categories = normalize_categories(data.get("categories", {}))
        rationale = str(data.get("rationale", rationale))
    except Exception:
        pass
    return ModerationDecision(allow=allow, categories=categories, rationale=rationale)
