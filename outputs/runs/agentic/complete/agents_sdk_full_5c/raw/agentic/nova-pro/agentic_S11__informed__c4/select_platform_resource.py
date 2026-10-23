import os
from ibm_watsonx_ai import WatsonxAI

# Set up the client
client = WatsonxAI(apikey=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))

# Select the model
model_id = client.select_model(model_family='meta-llama')

print(model_id)