import boto3

def answer_with_context(question, context):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(Text=context)
    return response['Languages'][0]['LanguageCode']