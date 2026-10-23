from typing import Optional
from model_client import get_llm_client
from model_models import ContextualAnswerRequest, ContextualAnswerResponse


def answer_with_context(
    question: str,
    context: str,
    model: Optional[str] = "gemini-1.5-pro-latest"
) -> str:
    """
    Answer a question using provided context via Google Gemini API.
    """
    client = get_llm_client()
    
    prompt = (
        f"Answer the question based only on the provided context. "
        f"If the answer is not in the context, say 'I don't know'.\n\n"
        f"Context: {context}\n\n"
        f"Question: {question}"
    )
    
    request = ContextualAnswerRequest(
        prompt=prompt,
        model=model
    )
    
    response = client.generate_content(
        model=request.model,
        prompt=request.prompt
    )
    
    return ContextualAnswerResponse.from_gemini(response).answer