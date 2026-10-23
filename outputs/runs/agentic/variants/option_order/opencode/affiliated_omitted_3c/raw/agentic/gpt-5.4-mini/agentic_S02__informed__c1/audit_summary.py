import boto3


def summarize_audit_events(events):
    bedrock = boto3.client("bedrock-runtime")
    prompt = "Summarize these federated-login audit events:\n" + "\n".join(
        str(e) for e in events
    )
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-sonnet-20240229-v1:0",
        body=(f"{'inputText': {prompt!r}}").encode(),
        contentType="application/json",
        accept="application/json",
    )
    return response.get("body")
