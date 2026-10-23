from openai import OpenAI
from model_client import get_client, get_model_name
from model_models import BuildTextRequest, JsonExtractionResult


def extract_json(text: str, schema_hint: str, *, model: str | None = None) -> JsonExtractionResult:
    client = get_client()
    model_name = model or get_model_name("extract")
    request = BuildTextRequest(task="extract_json", input_text=text, schema_hint=schema_hint)
    response = client.responses.create(model=model_name, input=request.to_prompt())
    output_text = response.output_text if hasattr(response, "output_text") else str(response)
    return JsonExtractionResult.from_text(output_text, model=model_name)
