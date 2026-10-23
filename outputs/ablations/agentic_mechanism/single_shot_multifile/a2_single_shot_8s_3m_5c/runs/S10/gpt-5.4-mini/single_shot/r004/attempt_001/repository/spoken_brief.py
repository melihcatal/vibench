from typing import Optional
from model_client import get_openai_client, select_text_model
from model_models import ChatPrompt, normalize_text_response


def spoken_brief(text: str, model: Optional[str] = None) -> str:
    client = get_openai_client()
    model_id = select_text_model(model=model, task="tts")
    prompt = ChatPrompt(
        system="You rewrite content into a short spoken briefing script.",
        user=f"Convert the following model output into a concise spoken brief suitable for audio narration:\n\n{text}",
    )
    response = client.chat.completions.create(
        model=model_id,
        messages=prompt.to_messages(),
        temperature=0.4,
    )
    return normalize_text_response(response)
