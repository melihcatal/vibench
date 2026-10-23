import google.generativeai as genai
import os

class LLMClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLMClient, cls).__new__(cls)
            cls._instance._configure()
        return cls._instance

    def _configure(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set.")
        genai.configure(api_key=api_key)

    def get_model(self, model_name: str):
        # This is a placeholder for model family selection.
        # In a real scenario, you might have different configurations for different models.
        if model_name.startswith("gemini"):
            return genai.GenerativeModel(model_name)
        else:
            raise ValueError(f"Unsupported model family: {model_name}")

def get_llm_client():
    return LLMClient()
