import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

def summarize_text(text):
    try:
        response = bedrock.invoke_model(
            model_id='amazon.bedrock.summarization-001',
            body={
                'text': text,
                'max_tokens': 150
            }
        )
        result = json.loads(response['body'].read())
        return result['summary']
    except (NoCredentialsError, PartialCredentialsError) as e:
        print(f'AWS credentials error: {e}')
        return None
    except Exception as e:
        print(f'An error occurred: {e}')
        return None

if __name__ == '__main__'):
    text_to_summarize = 'Long text to be summarized goes here...'
    summary = summarize_text(text_to_summarize)
    if summary:
        print(f'Summary: {summary}')
    else:
        print('Failed to generate summary.')