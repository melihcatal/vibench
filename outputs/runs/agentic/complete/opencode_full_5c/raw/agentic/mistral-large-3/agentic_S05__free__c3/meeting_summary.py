from google.cloud import aiplatform
from google.cloud.aiplatform.gapic import PredictionServiceClient
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from typing import List, Dict, Any


def summarize_meeting_chunks(transcript_chunks: List[str]) -> str:
    client = PredictionServiceClient(
        client_options={"api_endpoint": "us-central1-aiplatform.googleapis.com"}
    )
    endpoint = f"projects/{client.project}/locations/us-central1/publishers/google/models/text-bison@002"

    context = "Summarize the following meeting transcript in a concise manner:"
    prompt = f"{context}\n\n" + "\n".join(transcript_chunks)

    instance = json_format.ParseDict({"prompt": prompt}, Value())
    instances = [instance]
    parameters = json_format.ParseDict(
        {
            "temperature": 0.2,
            "maxOutputTokens": 256,
            "topK": 40,
            "topP": 0.95,
        },
        Value(),
    )

    response = client.predict(
        endpoint=endpoint, instances=instances, parameters=parameters
    )
    return response.predictions[0]["content"]


def meeting_summary(
    transcript_stream: AsyncIterable[Dict[str, Any]],
    chunk_size: int = 5,
) -> AsyncIterable[Dict[str, Any]]:
    buffer = []

    async for result in transcript_stream:
        if result["is_final"]:
            buffer.append(result["transcript"])
            if len(buffer) >= chunk_size:
                summary = summarize_meeting_chunks(buffer)
                yield {
                    "summary": summary,
                    "chunk_count": len(buffer),
                    "transcripts": buffer.copy(),
                }
                buffer.clear()

    if buffer:
        summary = summarize_meeting_chunks(buffer)
        yield {
            "summary": summary,
            "chunk_count": len(buffer),
            "transcripts": buffer.copy(),
        }
