import os
import boto3

def onboarding_summary(text):
    client = boto3.client(
        'comprehend',
        region_name=os.environ.get('AWS_REGION'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    try:
        key_phrases_response = client.detect_key_phrases(
            Text=text,
            LanguageCode='en'
        )
        entities_response = client.detect_entities(
            Text=text,
            LanguageCode='en'
        )

        key_phrases = [phrase['Text'] for phrase in key_phrases_response['KeyPhrases']]
        entities = [{'Text': entity['Text'], 'Type': entity['Type']} for entity in entities_response['Entities']]
        
        return {"key_phrases": key_phrases, "entities": entities}
    except Exception as e:
        return {"error": str(e)}
