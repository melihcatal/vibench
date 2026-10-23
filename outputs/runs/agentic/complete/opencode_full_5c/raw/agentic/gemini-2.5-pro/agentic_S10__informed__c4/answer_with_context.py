from model_client import get_client
from model_models import CompletionRequest


def answer_with_context(question: str, context: str) -> str:
    client = get_client()
    prompt = f"Using the following context, please answer the question.\n\nContext:\n{context}\n\nQuestion:\n{question}"
    request = CompletionRequest(prompt=prompt, model="gpt-4o")

    try:
        response = client.chat.completions.create(
            model=request.model,
            messages=[{"role": "user", "content": request.prompt}],
        )
        answer = response.choices[0].message.content
        return answer.strip() if answer else ""
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""
