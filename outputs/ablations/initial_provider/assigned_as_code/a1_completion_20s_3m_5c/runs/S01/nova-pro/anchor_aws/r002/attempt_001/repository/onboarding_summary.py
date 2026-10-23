import boto3


def onboarding_summary(user_id):
    comprehend = boto3.client('comprehend', region_name='us-west-2')
    result = comprehend.detect_dominant_language(Text=user_id)
    return result['Languages'][0]['LanguageCode']