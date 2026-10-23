import boto3


class StreamPlatformGeneration:
    def __init__(self, model_id):
        self.model_id = model_id
        self.bedrock = boto3.client('bedrock-runtime')

    def stream_output(self, prompt):
        response = self.bedrock.invoke_model(
            modelId=self.model_id,
            body={
                'prompt': prompt,
                'maxTokens': 500,
                'temperature': 0.7
            }
        )
        response_body = response['body'].read()
        response_json = json.loads(response_body)
        yield response_json['outputText']


if __name__ == '__main__':
    model_id = 'amazon.titan-text-express-v1'
    generator = StreamPlatformGeneration(model_id)
    prompt = 'Translate the following English text to French: Hello, how are you?'
    for output in generator.stream_output(prompt):
        print(output)