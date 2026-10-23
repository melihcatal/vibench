import os
from dotenv import load_dotenv
import openai

load_dotenv()  # loads .env with OPENAI_API_KEY
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embed_client() -> openai.Embedding:
    """Return an OpenAI embedding client configured for the project."""
    return openai.Embedding()