from typing import Iterator
from model_client import get_model
from model_models import GEMINI_MODEL_NAME

def stream_answer(prompt: str) -> Iterator[str]:
    """
    Streams partial output tokens from a hosted LLM for a given prompt.

    Args:
        prompt: The prompt to send to the model.

    Yields:
        A stream of text chunks from the model's response.
    """
    model = get_model(GEMINI_MODEL_NAME)
    
    try:
        response_stream = model.generate_content(prompt, stream=True)
        for chunk in response_stream:
            # The API may send empty chunks periodically.
            if chunk.text:
                yield chunk.text
    except Exception as e:
        print(f"An error occurred during streaming: {e}")
        yield "Error: Could not stream the response."
