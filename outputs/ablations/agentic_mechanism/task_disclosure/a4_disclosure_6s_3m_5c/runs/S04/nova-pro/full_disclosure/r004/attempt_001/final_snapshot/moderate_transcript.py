import boto3

def moderate_transcript(transcript_text):
    comprehend = boto3.client('comprehend')
    translate = boto3.client('translate')

    # Detect the language of the transcript
    language_response = translate.detect_dominant_language(Text=transcript_text)
    language_code = language_response['Languages'][0]['LanguageCode']

    # Detect inappropriate content
    response = comprehend.detect_sentiment(Text=transcript_text, LanguageCode=language_code)
    sentiment = response['Sentiment']

    if sentiment == 'NEGATIVE':
        return 'Transcript contains negative sentiment and may require moderation.'
    else:
        return 'Transcript is suitable for publishing.'