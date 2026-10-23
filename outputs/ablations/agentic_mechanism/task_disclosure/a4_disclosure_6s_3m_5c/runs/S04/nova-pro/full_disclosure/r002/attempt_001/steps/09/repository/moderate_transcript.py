import boto3

def moderate_transcript(transcript_text):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_toxic_content(
        TextSegments=[
            {
                'Text': transcript_text
            }
        ],
        LanguageCode='en'
    )
    if response['ResultList'][0]['Toxicity']['Label'] == 'TOXIC':
        return 'Moderation failed: Unsafe content detected'
    else:
        return 'Moderation passed: Safe content'
