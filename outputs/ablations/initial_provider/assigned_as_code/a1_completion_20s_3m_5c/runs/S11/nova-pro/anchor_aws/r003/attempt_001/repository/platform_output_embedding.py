import boto3

def embed_platform_output(output):
    comprehend = boto3.client('comprehend')
    response = comprehend.detect_dominant_language(
        Text=output
    )
    language_code = response['Languages'][0]['LanguageCode']
    embeddings = comprehend.detect_sentiment(
        Text=output,
        LanguageCode=language_code
    )
    return embeddings