import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def translation_memory_embedding(text):
    result = bedrock.invoke_model(ModelId="amazon.titan-embed-text-v1", Body=text)
    return result["Embedding"]
