import json

from model_client import create_openai_client, load_config, resolve_model
from model_models import (
    ExtractJsonRequest,
    ExtractJsonResponse,
    build_system_message,
    build_user_message,
)


def extract_json(
    text: str,
    schema_hint: str = "",
    model: str = "gpt-4o",
    temperature: float = 0.1,
) -> ExtractJsonResponse:
    req = ExtractJsonRequest(
        text=text,
        schema_hint=schema_hint,
        model=model,
        temperature=temperature,
    )
    config = load_config()
    resolved_model = resolve_model(req.model, config)
    client = create_openai_client()

    system_instruction = (
        "Extract structured JSON from the provided text. "
        "Return only valid JSON with no markdown formatting or extra text. "
    )
    if req.schema_hint:
        system_instruction += f"Match the following schema: {req.schema_hint}. "
    system_instruction += "If a field cannot be determined, use null."

    messages = [
        build_system_message(system_instruction),
        build_user_message(req.text),
    ]

    response = client.chat.completions.create(
        model=resolved_model,
        messages=messages,
        max_tokens=2048,
        temperature=req.temperature,
        response_format={"type": "json_object"},
    )

    raw_json = response.choices[0].message.content.strip()
    try:
        extracted = json.loads(raw_json)
    except json.JSONDecodeError:
        extracted = {}

    usage = {
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens,
        "total_tokens": response.usage.total_tokens,
    }

    return ExtractJsonResponse(
        extracted=extracted,
        raw_json=raw_json,
        model=response.model,
        usage=usage,
    )


if __name__ == "__main__":
    import sys

    input_text = sys.stdin.read() if not sys.stdin.isatty() else ""
    if input_text:
        result = extract_json(input_text)
        print(json.dumps(result.extracted, indent=2))
