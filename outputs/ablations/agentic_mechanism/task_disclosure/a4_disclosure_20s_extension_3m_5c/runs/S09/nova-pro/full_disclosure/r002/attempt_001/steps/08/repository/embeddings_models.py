import boto3

class EmbeddingsModel:
    def __init__(self, model_id='amazon.titan-embed-text-v1'):
        self.model_id = model_id
        self.client = boto3.client('bedrock-runtime')

    def create_request(self, input_text):
        return {
            'inputText': input_text
        }

    def send_request(self, request):
        response = self.client.invoke_model(
            modelId=self.model_id,
            body=request
        )
        return response

    def normalize_response(self, response):
        normalized_response = {
            'embedding': response['embedding']
        }
        return normalized_response
