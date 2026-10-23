import os
from mistralai.client import MistralClient

os.environ["MISTRAL_API_KEY"] = "your-mistral-api-key"

client = MistralClient(api_key=os.getenv('MISTRAL_API_KEY'))

def summarize_image(image_description):
    response = client.chat(model="mistral-large", messages=[{"role": "user", "content": image_description}])
    return response.choices[0].message.content