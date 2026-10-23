from google.cloud import aiplatform

from model_client import init_vertex_ai
from model_models import PlatformResponse, metadata_from_prediction, normalize_text


def collect_platform_metadata(prompt: str) -> PlatformResponse:
    config = init_vertex_ai()
    model = aiplatform.ChatModel.from_pretrained(config.model_name)
    chat = model.start_chat()
    response = chat.send_message(prompt)
    text = normalize_text(getattr(response, "text", response))
    metadata = metadata_from_prediction(getattr(response, "_prediction_response", None), config.model_name)
    return PlatformResponse(text=text, metadata=metadata)
