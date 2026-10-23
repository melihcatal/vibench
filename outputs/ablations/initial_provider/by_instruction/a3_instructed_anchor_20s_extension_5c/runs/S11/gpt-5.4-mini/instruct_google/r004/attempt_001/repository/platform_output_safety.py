from google.cloud import aiplatform

from model_client import init_vertex_ai


def platform_output_safety(text: str) -> bool:
    config = init_vertex_ai()
    model = aiplatform.ChatModel.from_pretrained(config.model_name)
    response = model.predict(text)
    return bool(getattr(response, "text", ""))
