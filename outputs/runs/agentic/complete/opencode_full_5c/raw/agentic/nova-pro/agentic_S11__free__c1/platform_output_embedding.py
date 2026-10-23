import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def embed_output(model_id, payload):
    response = bedrock.invoke_model(modelId=model_id, body=payload)
    # Placeholder for embedding logic
    return "Embedded output"


if __name__ == "__main__":
    model_id = "amazon.titan-text-express-v1"
    payload = {"inputText": "Hello, world!"}
    embedded_output = embed_output(model_id, payload)
    print(embedded_output)
