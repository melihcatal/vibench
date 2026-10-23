import boto3

def check_corpus_text(text):
    bedrock = boto3.client('bedrock')
    # Placeholder for actual text checking logic using Amazon Bedrock
    # This is a simplified example and should be replaced with actual implementation
    if 'sensitive' in text.lower():
        return 'Text contains sensitive information'
    else:
        return 'Text is safe for embedding'