from model_client import generate_text
from model_models import ModelRequest, ModelResponse

def summarize_text(long_text: str) -> str:
    """
    Calls a hosted LLM to summarize long text.
    """
    prompt = f"Please provide a concise summary of the following text:\n\n---\n{long_text}\n---"
    
    request = ModelRequest(prompt=prompt)
    response: ModelResponse = generate_text(request, model_name="gemini-1.5-flash")
    
    return response.text
