import os
from ibm_watsonx_ai import WatsonxAI

# Set up the client
client = WatsonxAI(apikey=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))

# Stream the generation
response = client.stream_generation(model_id='meta-llama/Llama-2-70b-chat-hf', input_text='Hello, world!')

for chunk in response:
    print(chunk)