import boto3

def embed_asset_metadata(bucket_name, object_key):
    comprehend_client = boto3.client('comprehend')
    s3_client = boto3.client('s3')
    object_metadata = s3_client.head_object(Bucket=bucket_name, Key=object_key)
    metadata_text = json.dumps(object_metadata)
    response = comprehend_client.detect_sentiment(Text=metadata_text, LanguageCode='en')
    return response