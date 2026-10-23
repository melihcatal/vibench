from model_client import HostedLLMClient
from model_models import LLMRequest, ModelConfig, normalize_messages


SYSTEM_PROMPT = (
    "You are a helpful assistant that answers questions based strictly on the provided context. "
    "If the answer cannot be determined from the context, say so clearly. "
    "Do not use outside knowledge."
)


def answer_with_context(
    question: str,
    context: str,
    model: str = "gpt-4o",
    temperature: float = 0.3,
    max_tokens: int = 500,
    config: ModelConfig | None = None,
) -> str:
    client = HostedLLMClient(config=config)
    user_content = f"Context:\n{context}\n\nQuestion: {question}\n\nAnswer:"
    messages = normalize_messages(user_content, system_prompt=SYSTEM_PROMPT)
    request = LLMRequest(
        messages=messages,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    response = client.chat_completion(request)
    return response.content


if __name__ == "__main__":
    context = (
        "The company was founded in 2015 by three engineers. "
        "It raised $50M in Series B funding in 2019. "
        "The headquarters is located in Austin, Texas. "
        "The current CEO is Maria Chen, who joined in 2020."
    )
    question = "When was the company founded and who is the current CEO?"
    result = answer_with_context(question, context)
    print(result)
