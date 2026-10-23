from openai import OpenAI
from model_client import get_openai_client, select_chat_model
from model_models import LLMRequest, normalize_text


def answer_with_context(question: str, context: str) -> str:
    client = get_openai_client()
    model = select_chat_model("qa")
    prompt = f"Context:
{normalize_text(context)}

Question:
{normalize_text(question)}"
    request = LLMRequest(task="qa", input_text=prompt, max_output_tokens=256)
    response = client.chat.completions.create(model=model, messages=[{"role": "system", "content": "Answer the question using only the provided context."}, {"role": "user", "content": request.input_text}], temperature=0.1, max_tokens=request.max_output_tokens)
    return response.choices[0].message.content or ""
