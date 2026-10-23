from google.cloud import aiplatform

from model_client import init_vertex_ai


def localized_platform_output(text: str, locale: str) -> str:
    config = init_vertex_ai()
    model = aiplatform.ChatModel.from_pretrained(config.model_name)
    chat = model.start_chat()
    response = chat.send_message(f"Translate to {locale}: {text}")
    return getattr(response, "text", str(response))
