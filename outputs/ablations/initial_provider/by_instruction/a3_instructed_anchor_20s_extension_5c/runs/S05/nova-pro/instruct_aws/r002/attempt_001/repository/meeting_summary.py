import boto3

def meeting_summary(transcript):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    result = comprehend.detect_dominant_language(Text=transcript)
    return result['Languages'][0]['LanguageCode']