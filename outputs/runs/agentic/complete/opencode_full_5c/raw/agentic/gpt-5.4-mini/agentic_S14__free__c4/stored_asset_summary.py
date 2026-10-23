from openai import OpenAI

from storage_client import get_bucket_name, get_object_key, get_s3_client


def stored_asset_summary(bucket=None, key=None):
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=get_bucket_name(bucket), Key=get_object_key(key))
    text = obj["Body"].read().decode("utf-8")
    client = OpenAI()
    response = client.responses.create(model="gpt-5.4-mini", input=f"Summarize: {text}")
    return response.output_text
