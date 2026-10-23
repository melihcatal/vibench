from storage_client import get_bedrock_client


def stored_asset_summary(text: str):
    bedrock = get_bedrock_client()
    body = '{"anthropic_version":"bedrock-2023-05-31","max_tokens":256,"messages":[{"role":"user","content":[{"type":"text","text":"Summarize this asset in one concise paragraph:\n" + text}]}]}'
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body,
        accept="application/json",
        contentType="application/json",
    )
    return {"summary": response["body"].read().decode("utf-8")}
