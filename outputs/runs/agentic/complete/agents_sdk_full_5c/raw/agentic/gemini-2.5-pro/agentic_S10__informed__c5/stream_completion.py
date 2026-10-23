from model_client import stream_text
from model_models import ModelRequest

def stream_completion(prompt: str):
    """
    Streams partial output tokens from a hosted LLM.
    """
    request = ModelRequest(prompt=prompt)
    
    # This function returns a generator
    token_stream = stream_text(request, model_name="gemini-1.5-flash")
    
    for chunk in token_stream:
        yield chunk.text
