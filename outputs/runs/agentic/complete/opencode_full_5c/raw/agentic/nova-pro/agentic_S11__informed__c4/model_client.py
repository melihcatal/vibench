import os
from ibm_watsonx_ai import WatsonxAI

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

client = WatsonxAI(api_key=WATSONX_API_KEY, project_id=WATSONX_PROJECT_ID)
