from google.cloud import aiplatform

from model_client import init_vertex_ai
from model_models import PlatformRequest, normalize_text


def invoke_platform_model(prompt: str) -> str:
    config = init_vertex_ai()
    model = aiplatform.ChatModel.from_pretrained(config.model_name)
    chat = model.start_chat()
    request = PlatformRequest(prompt=prompt)
    response = chat.send_message(request.prompt, temperature=request.temperature, max_output_tokens=request.max_output_tokens)
    return normalize_text(getattr(response, "text", response))
