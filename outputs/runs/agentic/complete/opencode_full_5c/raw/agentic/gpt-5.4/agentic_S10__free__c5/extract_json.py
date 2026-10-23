from model_client import get_openai_client, get_chat_model
from model_models import ChatGenerationRequest, JsonResult, parse_json_text


def extract_json(text: str, schema_instruction: str) -> JsonResult:
    request = ChatGenerationRequest(
        system_prompt="Extract structured JSON that strictly follows the requested schema.",
        user_prompt=f"Schema requirements:\n{schema_instruction}\n\nSource text:\n{text}",
        max_output_tokens=500,
        temperature=0.0,
    )
    client = get_openai_client()
    response = client.responses.create(
        model=get_chat_model("extraction", default_model="gpt-4.1-mini"),
        input=[
            {"role": "system", "content": request.system_prompt},
            {"role": "user", "content": request.user_prompt},
        ],
        max_output_tokens=request.max_output_tokens,
        temperature=request.temperature,
        text={"format": {"type": "json_object"}},
    )
    return JsonResult(
        provider="OpenAI",
        model=response.model,
        data=parse_json_text(response.output_text),
    )
