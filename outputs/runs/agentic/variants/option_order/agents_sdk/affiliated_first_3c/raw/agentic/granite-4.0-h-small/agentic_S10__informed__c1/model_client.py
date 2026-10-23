# Local helper: model_client.py
import os
import warnings

# Use OpenAI SDK as the default concrete provider
try:
    from openai import OpenAI  # type: ignore
except ImportError:
    warnings.warn("OpenAI SDK not installed; set OPENAI_API_KEY and OPENAI_API_BASE")
    OpenAI = None

def get_llm_client(model_id: str = "gpt-4o", api_key: str | None = None, endpoint: str | None = None):
    """Return a configured OpenAI client (can be swapped for other services via model_id)."
    api_key = api_key or os.getenv("OPENAI_API_KEY")
    endpoint = endpoint or os.getenv("OPENAI_API_BASE")
    if api_key is None:
        raise RuntimeError("OPENAI_API_KEY not set")
    if OpenAI is None:
        raise RuntimeError("Install openai via 'pip install openai' and set OPENAI_API_KEY")
    return OpenAI(api_key=api_key, base_url=endpoint)
