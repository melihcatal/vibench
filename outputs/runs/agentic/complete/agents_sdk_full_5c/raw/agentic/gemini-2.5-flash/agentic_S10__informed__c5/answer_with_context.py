from model_client import LLMClient
from model_models import LLMRequest, LLMResponse

def answer_with_context(question: str, context: str) -> LLMResponse:
    """Calls a hosted LLM to answer a question using provided context."""
    llm_client = LLMClient().get_client()
    model = llm_client.GenerativeModel('gemini-pro')

    prompt = (
        f"Given the following context, answer the question. "
        f"If the answer is not in the context, state that you don't know.\n\n"
        f"Context:\n{context}\n\n"
        f"Question:\n{question}\n\n"
        f"Answer:"
    )

    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "max_output_tokens": 500,
        }
    )
    return LLMResponse(text=response.text, raw_response=response)
