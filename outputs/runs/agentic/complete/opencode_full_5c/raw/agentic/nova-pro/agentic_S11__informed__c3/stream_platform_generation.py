import boto3

AWS_REGION = "us-west-2"
MODEL_ID = "amazon.titan-text-express-v1"

bedrock_client = boto3.client("bedrock-runtime", region_name=AWS_REGION)


def stream_generation(prompt):
    response = bedrock_client.invoke_model(
        modelId=MODEL_ID,
        body={
            "inputText": prompt,
            "textGenerationConfig": {
                "maxTokenCount": 500,
                "temperature": 0.5,
                "topP": 0.9,
            },
        },
    )
    for event in response["body"]["chunks"]:
        yield event["text"]
