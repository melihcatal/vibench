from openai import OpenAI
from model_client import get_openai_client, select_chat_model
from model_models import LLMRequest, LLMResponse, normalize_text


def summarize_text(text: str, max_output_tokens: int = 256) -> str:
    client = get_openai_client()
    model = select_chat_model("summarization")
    request = LLMRequest(task="summarization", input_text=normalize_text(text), max_output_tokens=max_output_tokens)
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Summarize the provided text concisely."}, {"role": "user", "content": request.input_text}], temperature=0.2, max_tokens=request.max_output_tokens)
    content = response.choices[0].message.content or ""
    return LLMResponse(text=content).text
