from model_client import get_openai_client
from model_models import LLMRequest, LLMResponse, ChatMessage
import json


def extract_json(text: str) -> LLMResponse:
    client = get_openai_client()
    prompt_message = ChatMessage(
        role="user",
        content=f"Extract all structured data as a JSON object from the following text: {text}. Respond with only the JSON object.",
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": msg.role, "content": msg.content} for msg in [prompt_message]
        ],
        response_format={"type": "json_object"},
        max_tokens=500,
    )
    json_data = response.choices[0].message.content.strip()
    return LLMResponse(
        text=json_data, model=response.model, usage=response.usage.model_dump()
    )
