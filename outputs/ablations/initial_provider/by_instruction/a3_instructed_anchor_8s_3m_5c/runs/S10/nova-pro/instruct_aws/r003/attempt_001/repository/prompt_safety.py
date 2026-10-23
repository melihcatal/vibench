import boto3

def check_prompt_safety(prompt):
    client = boto3.client('comprehend')
    response = client.detect_toxic_content(
        TextSegments=[{
            'Text': prompt
        }],
        LanguageCode='en'
    )
    return response.get('ResultList')[0].get('Toxicity')