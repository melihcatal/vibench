from model_client import complete_chat
from model_models import LLMRequest

QA_MODEL = "gpt-4o-mini"


def answer_with_context(question: str, context: str) -> str:
    request = LLMRequest(
        prompt=question,
        context=context,
        system="Answer using only the provided context. If the answer is not present, say so.",
        model=QA_MODEL,
        temperature=0.2,
        max_tokens=256,
    )
    return complete_chat(request).text
