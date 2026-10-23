import boto3

class EmbeddingsClient:
    def __init__(self, region_name='us-west-2'):
        self.bedrock = boto3.client('bedrock', region_name=region_name)

    def get_embeddings(self, text):
        response = self.bedrock.invoke_model(
            model_id='amazon.titan-embed-text-v1',
            body={
                'inputText': text
            }
        )
        return response['embedding']