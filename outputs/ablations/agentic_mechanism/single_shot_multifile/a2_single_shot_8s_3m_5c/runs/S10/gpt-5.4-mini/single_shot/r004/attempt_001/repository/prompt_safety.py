import json
from typing import Any, Dict, Optional
from model_client import get_openai_client, select_text_model
from model_models import ChatPrompt, normalize_text_response, normalize_safety_result


def prompt_safety(prompt: str, generated_text: Optional[str] = None, model: Optional[str] = None) -> Dict[str, Any]:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="safety")
    payload = prompt if generated_text is None else f"Prompt:\n{prompt}\n\nGenerated text:\n{generated_text}"
    system = "You assess whether content is unsafe. Return strict JSON with flagged and categories."
    response = client.chat.completions.create(
        model=model_id,
        messages=ChatPrompt(system=system, user=payload).to_messages(),
        temperature=0,
        response_format={"type": "json_object"},
    )
    content = normalize_text_response(response)
    data: Dict[str, Any] = json.loads(content)
    return normalize_safety_result(prompt if generated_text is None else generated_text, data.get("flagged", False), data.get("categories", {}))
