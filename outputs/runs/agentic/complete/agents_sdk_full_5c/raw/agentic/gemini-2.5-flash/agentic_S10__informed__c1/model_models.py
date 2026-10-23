class GeminiModelConfig:
    """
    A simple configuration class for Gemini models.
    """
    def __init__(self, model_name: str, temperature: float = 0.7, top_p: float = 0.9, top_k: int = 40):
        self.model_name = model_name
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k

    def __repr__(self):
        return f"GeminiModelConfig(model_name='{self.model_name}', temperature={self.temperature}, top_p={self.top_p}, top_k={self.top_k})"

# Pre-defined model family identifiers
GEMINI_PRO = "gemini-pro"
GEMINI_FLASH = "gemini-pro-vision" # Placeholder for a vision model, adjust if pure text-flash is available
EMBEDDING_001 = "models/embedding-001"
