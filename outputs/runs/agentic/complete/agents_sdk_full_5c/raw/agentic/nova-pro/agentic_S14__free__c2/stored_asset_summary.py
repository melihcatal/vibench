import boto3
from gensim.summarization import summarize

s3 = boto3.client('s3')

def stored_asset_summary(bucket_name, object_name):
    response = s3.get_object(Bucket=bucket_name, Key=object_name)
    text_content = response['Body'].read().decode('utf-8')
    summary = summarize(text_content)
    return summary