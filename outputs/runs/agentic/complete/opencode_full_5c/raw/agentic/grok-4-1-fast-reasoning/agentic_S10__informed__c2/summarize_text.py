import os
from openai import OpenAI
import model_client
import model_models
from typing import Dict, Any


def summarize_text(text: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = model_client.get_default_model()
    system_prompt = "You are an expert summarizer. Provide concise, accurate summaries capturing key points."
    user_prompt = f"Summarize this text:\n\n{text}"
    messages = model_models.build_messages(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model=model, messages=messages, max_tokens=1000, temperature=0.1
    )
    return response.choices[0].message.content.strip()
