# translation_client.py
from openai import OpenAI

# Load credentials from environment for the concrete provider (OpenAI)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY environment variable not set")

client = OpenAI(api_key=OPENAI_API_KEY)

def get_translation_client() -> OpenAI:
    """Return a configured OpenAI client for translation tasks."""
    return client
