import boto3


def summarize_text(text):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        model_id="amazon.titan-text-express-v1",
        body={
            "inputText": text,
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
                "topP": 0.9,
            },
        },
    )
    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]
