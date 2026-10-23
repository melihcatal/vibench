import boto3


def answer_with_context(question, context):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        model_id="amazon.titan-text-express-v1",
        body={
            "inputText": f"{context} {question}",
            "textGenerationConfig": {
                "maxTokenCount": 512,
                "temperature": 0.5,
                "topP": 0.9,
            },
        },
    )
    return response["outputText"]
