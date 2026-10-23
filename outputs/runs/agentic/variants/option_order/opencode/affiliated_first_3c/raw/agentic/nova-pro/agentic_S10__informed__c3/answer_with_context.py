import boto3


def answer_with_context(question, context):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        model_id="amazon.titan-text-express-v1",
        body={
            "inputText": f"{context} {question}",
            "textGenerationConfig": {
                "maxTokenCount": 200,
                "stopSequences": [],
                "temperature": 0.5,
                "topP": 0.9,
            },
        },
    )
    result = json.loads(response["body"].read())
    return result["results"][0]["outputText"]
