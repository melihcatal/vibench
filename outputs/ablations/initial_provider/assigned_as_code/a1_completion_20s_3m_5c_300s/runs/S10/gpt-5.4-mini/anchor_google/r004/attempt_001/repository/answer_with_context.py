import os

from google import genai

from model_client import build_model_config, build_prompt, get_api_key


def answer_with_context(payload, config=None):
    config = build_model_config(config)
    prompt = build_prompt(
        "Answer the question using only the provided context. If the answer is not in the context, say you do not know.",
        payload.get("context", "") + "\n\nQuestion: " + payload.get("question", ""),
    )
    with genai.Client(api_key=get_api_key(config, "GOOGLE_API_KEY")) as client:
        response = client.models.generate_content(model=config["model"], contents=prompt)
    return {"text": response.text or ""}
