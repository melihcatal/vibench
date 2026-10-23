import boto3

from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class AnswerWithContext:
    def __init__(self, region_name='us-west-2'):
        self.region_name = region_name
        self.bedrock = boto3.client('bedrock-runtime', region_name=self.region_name)

    def answer_question(self, question, context):
        try:
            response = self.bedrock.invoke_model(
                modelId='amazon.titan-text-express-v1',
                body={
                    'inputText': f"Answer the following question using the provided context: {question}. Context: {context}",
                    'textGenerationConfig': {
                        'maxTokenCount': 4096,
                        'stopSequences': [],
                        'temperature': 0.5,
                        'topP': 0.9
                    }
                }
            )
            result = json.loads(response['body'].read())
            return result['results'][0]['outputText']
        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Error: {e}")
            return None


if __name__ == '__main__':
    answerer = AnswerWithContext()
    question = 'What is the capital of France?'
    context = 'France is a country in Europe. The capital of France is Paris.'
    answer = answerer.answer_question(question, context)
    print(f"Answer: {answer}")