from model_client import get_model
from model_models import GEMINI_MODEL_NAME

def summarize(text: str) -> str:
    """
    Summarizes the given text using a hosted LLM.

    Args:
        text: The text to summarize.

    Returns:
        The summarized text.
    """
    model = get_model(GEMINI_MODEL_NAME)
    prompt = f"Please provide a concise summary of the following text:\n\n---\n{text}\n---"
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during summarization: {e}")
        return ""
