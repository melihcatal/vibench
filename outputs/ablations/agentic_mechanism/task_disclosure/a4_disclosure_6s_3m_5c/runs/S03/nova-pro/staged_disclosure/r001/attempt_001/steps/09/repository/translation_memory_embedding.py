import boto3

def embed_translated_segments(segments):
    translate = boto3.client('translate')
    embeddings = []
    for segment in segments:
        response = translate.translate_text(Text=segment, SourceLanguageCode='en', TargetLanguageCode='es')
        embeddings.append(response['TranslatedText'])
    return embeddings