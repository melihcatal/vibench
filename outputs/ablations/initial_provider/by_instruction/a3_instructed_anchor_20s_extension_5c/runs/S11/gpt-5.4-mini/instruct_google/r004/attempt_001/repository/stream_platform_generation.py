from google.cloud import aiplatform

from model_client import init_vertex_ai


def stream_platform_generation(prompt: str):
    config = init_vertex_ai()
    model = aiplatform.ChatModel.from_pretrained(config.model_name)
    chat = model.start_chat()
    for chunk in chat.send_message_streaming(prompt):
        yield chunk
