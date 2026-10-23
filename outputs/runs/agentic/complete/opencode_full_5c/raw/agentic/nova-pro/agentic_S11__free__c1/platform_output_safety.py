import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")


def check_safety(model_id, payload):
    response = bedrock.invoke_model(modelId=model_id, body=payload)
    # Placeholder for safety check logic
    return True


if __name__ == "__main__":
    model_id = "amazon.titan-text-express-v1"
    payload = {"inputText": "Hello, world!"}
    is_safe = check_safety(model_id, payload)
    print(is_safe)
