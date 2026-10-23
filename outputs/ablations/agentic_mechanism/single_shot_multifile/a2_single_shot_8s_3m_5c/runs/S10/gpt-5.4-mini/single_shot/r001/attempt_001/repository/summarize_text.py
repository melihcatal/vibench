from openai import OpenAI
from model_client import get_chat_client, resolve_text_model
from model_models import ChatRequest, TextSummary, normalize_text_output, extract_message_text


def summarize_text(text: str, max_sentences: int = 5) -> str:
    client = get_chat_client()
    model = resolve_text_model()
    request = ChatRequest(
        model=model,
        system_prompt='You are a concise assistant that summarizes text.',
        user_prompt=f'Summarize the following text in at most {max_sentences} sentences. Preserve key facts and names.\n\n{text}',
        temperature=0.2,
    )
    response = client.chat.completions.create(**request.to_kwargs())
    content = extract_message_text(response)
    return normalize_text_output(content)
