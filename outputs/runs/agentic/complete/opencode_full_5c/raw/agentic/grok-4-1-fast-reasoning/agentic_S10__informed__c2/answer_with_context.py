import os
from openai import OpenAI
import model_client
import model_models


def answer_with_context(context: str, question: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = model_client.get_default_model()
    system_prompt = "You are a helpful assistant. Answer questions accurately using only the provided context. If the answer is not in the context, say so."
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    messages = model_models.build_messages(system_prompt, user_prompt)
    response = client.chat.completions.create(
        model=model, messages=messages, max_tokens=1000, temperature=0.1
    )
    return response.choices[0].message.content.strip()
