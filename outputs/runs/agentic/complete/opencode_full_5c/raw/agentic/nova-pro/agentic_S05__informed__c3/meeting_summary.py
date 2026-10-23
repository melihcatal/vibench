import boto3

bedrock_client = boto3.client("bedrock-runtime", region_name="us-west-2")


def summarize_transcript(transcript):
    response = bedrock_client.invoke_model(
        modelId="amazon.titan-text-express-v1",
        body={
            "inputText": transcript,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
                "topP": 0.9,
            },
        },
    )
    return response["body"].read().decode()
