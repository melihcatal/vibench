import boto3
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
s3 = boto3.client('s3')

def asset_metadata_embedding(bucket_name, object_name):
    response = s3.get_object(Bucket=bucket_name, Key=object_name)
    text_content = response['Body'].read().decode('utf-8')
    embedding = model.encode(text_content)
    return embedding