import os
from ibm_watsonx_ai import Client

class Extractor:
    def __init__(self):
        self.client = Client(instance_url=os.getenv('WATSONX_INSTANCE_URL'), api_key=os.getenv('WATSONX_API_KEY'), project_id=os.getenv('WATSONX_PROJECT_ID'))
        self.model_id = 'granite-4.0-h-small'

    def extract(self, prompt, max_tokens=150):
        payload = {
            'model_id': self.model_id,
            'inputs': prompt,
            'parameters': {
                'max_new_tokens': max_tokens,
                'temperature': 0.2,
                'response_format': 'json'
            }
        }
        response = self.client.text_chat(completion=payload)
        return response['generated_text']

if __name__ == '__main__':
    extractor = Extractor()
    sample = 'Extract the key details as JSON: """sample text""" 
    print(extractor.extract(sample))
