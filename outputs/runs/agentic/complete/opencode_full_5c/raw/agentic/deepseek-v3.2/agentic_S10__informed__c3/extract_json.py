import json
from model_client import ModelClient
from model_models import (
    ChatMessage,
    CompletionRequest,
    CompletionResponse,
    parse_json_response,
)


def extract_json(text: str, schema_description: str) -> dict:
    client = ModelClient()

    prompt = f"""Extract structured data from the following text according to this schema description: {schema_description}

Text to extract from:
{text}

Return ONLY a valid JSON object that matches the schema description. Do not include any explanatory text."""

    messages = [
        ChatMessage(
            role="system",
            content="You are a helpful assistant that extracts structured JSON data from text. Always return valid JSON.",
        ),
        ChatMessage(role="user", content=prompt),
    ]

    request = CompletionRequest(
        messages=messages, model="gpt-4o", temperature=0.1, max_tokens=1000
    )

    response = client.create_completion(
        messages=request.messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
        response_format={"type": "json_object"},
    )

    result = CompletionResponse.from_openai_response(response)

    try:
        return parse_json_response(result.content)
    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON", "raw_response": result.content}
