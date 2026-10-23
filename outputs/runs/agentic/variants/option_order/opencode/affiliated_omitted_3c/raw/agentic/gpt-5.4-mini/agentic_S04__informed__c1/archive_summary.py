import boto3


def archive_summary(transcript_text: str):
    client = boto3.client("bedrock-runtime")
    body = {"inputText": f"Summarize the following transcript:

{transcript_text}"}
    resp = client.invoke_model(modelId="amazon.titan-text-express-v1", body=__import__("json").dumps(body), accept="application/json", contentType="application/json")
    return resp["body"].read().decode("utf-8")
