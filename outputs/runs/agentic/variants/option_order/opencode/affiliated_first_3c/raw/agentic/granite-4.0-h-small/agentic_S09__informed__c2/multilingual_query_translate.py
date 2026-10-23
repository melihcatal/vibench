# multilingual_query_translate.py
# [LATER-STEP] Translate multilingual queries before embedding search

import os
from embeddings_client import get_watsonx_client
from ibm_watsonx_ai.services import Translation

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

t_client = Translation(client=get_watsonx_client())


def translate_query(query: str, target_lang: str = "en") -> str:
    """Translate a query to the target language using WatsonX translation service."""
    response = t_client.translate(
        text=[query], target_language=target_lang, model_id="en->zh"
    )
    # Assuming response format contains translations under 'translations'
    return response[0].get("translation", query)
