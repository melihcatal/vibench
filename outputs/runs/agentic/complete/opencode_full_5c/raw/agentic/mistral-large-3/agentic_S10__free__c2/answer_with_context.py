from model_client import ModelClient


def answer_with_context(
    question: str, context: str, max_tokens: int = 500, temperature: float = 0.5
) -> str:
    client = ModelClient()
    return client.answer_with_context(question, context, max_tokens, temperature)
