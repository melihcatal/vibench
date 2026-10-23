import boto3

def check_corpus_text(text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': text
            }
        ]
    )
    toxic_content_detected = any(result['Toxicity'] > 0.5 for result in response['Results'])
    return not toxic_content_detected