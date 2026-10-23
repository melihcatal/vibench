import boto3

def embed_moderation_rationales(rationales):
    comprehend = boto3.client('comprehend')
    embeddings = []
    for rationale in rationales:
        response = comprehend.detect_dominant_language(Text=rationale)
        embeddings.append(response['Languages'][0]['LanguageCode'])
    return embeddings
