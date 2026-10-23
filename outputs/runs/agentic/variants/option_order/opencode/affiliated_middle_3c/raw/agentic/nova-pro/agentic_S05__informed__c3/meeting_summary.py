import boto3


def summarize_meeting(transcript: str):
    bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")
    response = bedrock.invoke_model(
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
    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]
