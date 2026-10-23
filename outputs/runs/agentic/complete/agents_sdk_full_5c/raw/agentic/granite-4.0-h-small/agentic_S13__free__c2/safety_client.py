import os

class SafetyClient:
    """Local helper that abstracts configuration and calls to the Text Content Safety provider."""
    _MODEL = "openai/moderations"
    _API_BASE = os.getenv('SAFETY_API_BASE', 'https://api.openai.com/v1')

    @classmethod
    def create_moderation(cls, input: str) -> dict:
        """Call the provider's moderation endpoint (here represented by the OpenAI SDK)."""
        # Using the openai Python SDK as the concrete provider integration.
        import openai
        openai.api_base = cls._API_BASE
        openai.api_key = os.getenv('OPENAI_API_KEY')
        response = openai.Moderation.create(input=input, model=cls._MODEL)
        return response


def get_safety_client() -> SafetyClient:
    """Factory returning a thread‑safe singleton client instance."""
    return SafetyClient()
