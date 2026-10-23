import boto3


def archive_summary(payload, config=None):
    config = config or {}
    client = boto3.client("bedrock-runtime", region_name=config.get("region"))
    transcript_text = payload.get("text") or " ".join(segment.get("text", "") for segment in payload.get("segments", []))
    model_id = config.get("model_id") or "anthropic.claude-3-haiku-20240307-v1:0"
    response = client.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": f"Summarize this transcript in 3 bullets:\n{transcript_text}"}],
            }
        ],
    )
    output = response.get("output", {}).get("message", {}).get("content", [])
    summary = " ".join(part.get("text", "") for part in output if isinstance(part, dict))
    return {"summary": summary, "model_id": model_id, "job_id": payload.get("job_id")}
