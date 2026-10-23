import boto3


def stream_completion(text):
    client = boto3.client("bedrock-runtime")
    response = client.invoke_model(
        model_id="amazon.titan-text-express-v1",
        body={
            "inputText": text,
            "textGenerationConfig": {
                "maxTokenCount": 200,
                "stopSequences": [],
                "temperature": 0.5,
                "topP": 0.9,
            },
        },
    )
    result = json.loads(response["body"].read())
    for output in result["results"]:
        yield output["outputText"]
