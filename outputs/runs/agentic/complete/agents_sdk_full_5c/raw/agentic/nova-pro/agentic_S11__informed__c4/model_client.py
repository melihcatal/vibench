import os
from ibm_watsonx_ai import WatsonxAI

# Set up the client
def get_client():
    return WatsonxAI(apikey=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))