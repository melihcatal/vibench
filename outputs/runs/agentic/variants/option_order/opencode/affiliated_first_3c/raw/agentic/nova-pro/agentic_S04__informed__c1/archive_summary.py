import boto3

BEDROCK_CLIENT = boto3.client("bedrock-runtime")


def summarize_transcript(transcript):
    model_id = "amazon.titan-text-express-v1"
    body = {
        "inputText": transcript,
        "textGenerationConfig": {"maxTokenCount": 512, "temperature": 0.5, "topP": 0.9},
    }
    response = BEDROCK_CLIENT.invoke_model(
        body=json.dumps(body),
        modelId=model_id,
        accept="application/json",
        contentType="application/json",
    )
    result = json.loads(response.get("body").read())
    return result["results"][0]["outputText"]
