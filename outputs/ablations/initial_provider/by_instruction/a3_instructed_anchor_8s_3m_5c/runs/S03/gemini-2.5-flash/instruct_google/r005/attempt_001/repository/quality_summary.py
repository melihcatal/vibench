import boto3

def summarize_quality_issues(text: str) -> str:
    client = boto3.client('comprehend', region_name='us-east-1') # Replace with your desired region

    response = client.detect_key_phrases(Text=text, LanguageCode='en') # Assuming English for quality issue descriptions
    key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]

    # For a simple summary, we can join the key phrases. 
    # A more sophisticated approach would involve more advanced NLP or a different Comprehend feature.
    summary = "Translation quality issues identified: " + ", ".join(key_phrases)
    if not key_phrases:
        summary = "No specific translation quality issues identified based on key phrase extraction."

    return summary
