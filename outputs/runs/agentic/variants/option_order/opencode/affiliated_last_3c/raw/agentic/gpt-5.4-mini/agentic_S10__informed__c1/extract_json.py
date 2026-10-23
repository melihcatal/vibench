from openai import OpenAI

from model_client import build_messages, get_model_name, get_openai_client
from model_models import LLMRequest, extract_json_object, normalize_text


def extract_json(text: str) -> dict:
    req = LLMRequest(
        prompt=normalize_text(text),
        system="Extract structured JSON from the text. Return only valid JSON.",
        max_output_tokens=512,
        model=get_model_name(),
    )
    client: OpenAI = get_openai_client()
    response = client.chat.completions.create(
        model=req.model,
        messages=build_messages(req.system, req.prompt),
        temperature=0,
        max_tokens=req.max_output_tokens,
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or "{}"
    parsed = extract_json_object(content)
    if "raw" in parsed:
        return parsed
    return parsed
