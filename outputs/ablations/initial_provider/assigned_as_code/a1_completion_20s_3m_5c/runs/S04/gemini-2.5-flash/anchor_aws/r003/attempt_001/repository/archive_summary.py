import json
from typing import List, Dict, Any

from speech_client import SpeechClient
from speech_models import TranscriptSegment

def archive_summary(segments: List[TranscriptSegment], config: dict = None) -> Dict[str, Any]:
    config = config or {}
    region = config.get("region")
    if not region:
        raise ValueError("AWS region must be provided in config.")

    speech_client = SpeechClient(region_name=region)
    bedrock_runtime_client = speech_client.get_bedrock_runtime_client()

    full_transcript_text = " ".join([s.content for s in segments])

    # Using Anthropic Claude on Amazon Bedrock for summarization
    # Model ID can vary, using a common one for example
    model_id = config.get("bedrock_model_id", "anthropic.claude-v2")

    prompt = f"Human: Summarize the following meeting transcript:\n\n<transcript>\n{full_transcript_text}\n</transcript>\n\nAssistant:"

    body = json.dumps({
        "prompt": prompt,
        "max_tokens_to_sample": 1000,
        "temperature": 0.1,
        "top_p": 0.9
    })

    try:
        response = bedrock_runtime_client.invoke_model(
            body=body,
            modelId=model_id,
            accept="application/json",
            contentType="application/json"
        )
        response_body = json.loads(response.get("body").read())
        summary = response_body.get("completion")
        return {"summary": summary}
    except Exception as e:
        print(f"Error summarizing transcript: {e}")
        return {"summary": f"Error generating summary: {e}"}
