import boto3

def embed_text(text):
    comprehend_client = boto3.client('comprehend')
    response = comprehend_client.detect_dominant_language(
        Text=text
    )
    return response

if __name__ == '__main__':
    print(embed_text('This is a sample text to embed.'))