from observability_client import get_vertex_ai_model
from observability_models import SafetyAttributes
from typing import Any, Dict

def check_log_message_safety(message_text: str) -> SafetyAttributes:
    model = get_vertex_ai_model("gemini-pro")

    prompt = f"Analyze the safety of the following log message: {message_text}"

    response = model.generate_content(
        prompt,
        safety_settings=[],
        generation_config={"max_output_tokens": 1}
    )
    
    safety_ratings = None
    blocked = False
    categories_scores: Dict[str, float] = {}

    if response.candidates:
        candidate = response.candidates[0]
        if candidate.safety_ratings:
            safety_ratings = candidate.safety_ratings
            for rating in safety_ratings:
                categories_scores[rating.category.name] = rating.probability.value
            blocked = any(r.probability.value >= 3 for r in safety_ratings) # 3:HIGH, 4:VERY_HIGH
    elif response.prompt_feedback and response.prompt_feedback.block_reason:
        blocked = True

    return SafetyAttributes(
        categories=categories_scores,
        blocked=blocked,
        safety_ratings=safety_ratings
    )