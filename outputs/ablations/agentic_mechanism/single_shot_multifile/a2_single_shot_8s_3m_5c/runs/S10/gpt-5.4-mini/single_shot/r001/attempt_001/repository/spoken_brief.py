from openai import OpenAI
from model_client import get_chat_client, resolve_text_model
from model_models import ChatRequest, extract_message_text


def spoken_brief(model_output: str) -> str:
    client = get_chat_client()
    model = resolve_text_model()
    request = ChatRequest(
        model=model,
        system_prompt='You rewrite content as a short spoken briefing suitable for text-to-speech.',
        user_prompt=f'Create a concise spoken brief from the following model output:\n\n{model_output}',
        temperature=0.3,
    )
    response = client.chat.completions.create(**request.to_kwargs())
    return extract_message_text(response)
