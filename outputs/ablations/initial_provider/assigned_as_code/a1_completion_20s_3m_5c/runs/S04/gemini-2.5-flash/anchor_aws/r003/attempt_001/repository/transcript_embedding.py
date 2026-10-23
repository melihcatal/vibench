import json
from typing import List, Dict, Any

from speech_client import SpeechClient
from speech_models import TranscriptSegment

def transcript_embedding(segments: List[TranscriptSegment], config: dict = None) -> List[Dict[str, Any]]:
    config = config or {}
    region = config.get("region")
    if not region:
        raise ValueError("AWS region must be provided in config.")

    speech_client = SpeechClient(region_name=region)
    bedrock_runtime_client = speech_client.get_bedrock_runtime_client()

    # Using Amazon Titan Embeddings G1 - Text on Amazon Bedrock
    model_id = config.get("bedrock_embedding_model_id", "amazon.titan-embed-text-v1")

    embedded_segments = []
    for segment in segments:
        text_to_embed = segment.content
        body = json.dumps({"inputText": text_to_embed})

        try:
            response = bedrock_runtime_client.invoke_model(
                body=body,
                modelId=model_id,
                accept="application/json",
                contentType="application/json"
            )
            response_body = json.loads(response.get("body").read())
            embedding = response_body.get("embedding")
            embedded_segments.append({
                "segment_content": segment.content,
                "embedding": embedding,
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "speaker_label": segment.speaker_label
            })
        except Exception as e:
            print(f"Error embedding segment: {e}")
            embedded_segments.append({
                "segment_content": segment.content,
                "embedding": None,
                "error": str(e),
                "start_time": segment.start_time,
                "end_time": segment.end_time,
                "speaker_label": segment.speaker_label
            })

    return embedded_segments
