from model_client import ModelClient
from model_models import ChatMessage, CompletionRequest, CompletionResponse


def answer_with_context(question: str, context: str) -> str:
    client = ModelClient()

    prompt = f"""Based on the following context, answer the question. If the answer cannot be found in the context, say "I cannot answer based on the provided context."

Context:
{context}

Question: {question}

Answer:"""

    messages = [
        ChatMessage(
            role="system",
            content="You are a helpful assistant that answers questions based only on the provided context.",
        ),
        ChatMessage(role="user", content=prompt),
    ]

    request = CompletionRequest(
        messages=messages, model="gpt-4o", temperature=0.3, max_tokens=500
    )

    response = client.create_completion(
        messages=request.messages,
        model=request.model,
        temperature=request.temperature,
        max_tokens=request.max_tokens,
    )

    result = CompletionResponse.from_openai_response(response)
    return result.content.strip()
