from model_client import generate_text
from model_models import ModelRequest, ModelResponse

def answer_with_context(question: str, context: str) -> str:
    """
    Calls a hosted LLM to answer a question using provided context.
    """
    prompt = f"Answer the following question based *only* on the provided context.\n\nQuestion: {question}"
    
    request = ModelRequest(prompt=prompt, context=context)
    response: ModelResponse = generate_text(request, model_name="gemini-1.5-flash")
    
    return response.text
