import boto3
import embed


def embed_object_metadata_and_text(object_name, config=None):
    config = config or {}
    client = boto3.client('s3', region_name=config.get('region'))
    response = client.get_object(Bucket=config['bucket'], Key=object_name)
    document_content = response['Body'].read()
    text = document_content.decode('utf-8')
    metadata = client.head_object(Bucket=config['bucket'], Key=object_name)
    embedding = embed.embed(metadata, text)
    return embedding