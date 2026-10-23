from openai import OpenAI
from model_client import get_openai_client, select_chat_model
from model_models import LLMRequest, parse_json_object, normalize_text


def extract_json(text: str) -> dict:
    client = get_openai_client()
    model = select_chat_model("structured_extraction")
    request = LLMRequest(task="structured_extraction", input_text=normalize_text(text), max_output_tokens=512)
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Extract the relevant information as strict JSON only."}, {"role": "user", "content": request.input_text}], temperature=0.0, max_tokens=request.max_output_tokens, response_format={"type": "json_object"})
    content = response.choices[0].message.content or "{}"
    return parse_json_object(content)
