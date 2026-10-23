from model_client import get_gemini_model
from model_models import *

def summarize_text(text: str) -> str:
    model = get_gemini_model("gemini-pro") # Concrete model identifier
    response = model.generate_content(f"Summarize the following text: {text}")
    return response.text
