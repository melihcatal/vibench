import os
from ibm_watsonx_ai.services.translation import Translation
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

translator = Translation(
    api_key=API_KEY,
    project_id=PROJECT_ID,
    url="https://api.us-south.watsonx.ai"
)

def get_translator() -> Translation:
    """Return a configured translation client."""
    return translator

def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query before multilingual embedding search."""
    result = get_translator().translate(text=query, target_lang=target_lang)
    return result['translation'][0]['message']
