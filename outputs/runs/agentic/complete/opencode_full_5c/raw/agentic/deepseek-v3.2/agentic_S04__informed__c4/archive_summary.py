import os
import json
from typing import Dict, Any, List
import boto3
from botocore.exceptions import ClientError


def summarize_transcription_results(
    transcript_text: str, max_summary_length: int = 200
) -> Dict[str, Any]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    if not transcript_text.strip():
        return {"summary": "", "key_points": [], "word_count": 0, "summary_length": 0}

    prompt = f"""Please provide a concise summary of the following transcript in {max_summary_length} words or less:

{transcript_text}

Summary:"""

    try:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 500,
                "messages": [{"role": "user", "content": prompt}],
            }
        )

        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body,
            contentType="application/json",
        )

        response_body = json.loads(response["body"].read())
        summary = response_body.get("content", [{}])[0].get("text", "").strip()

        key_points_prompt = f"""Extract 3-5 key points from this transcript:

{transcript_text}

Key points:"""

        key_points_body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 300,
                "messages": [{"role": "user", "content": key_points_prompt}],
            }
        )

        key_points_response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=key_points_body,
            contentType="application/json",
        )

        key_points_body_content = json.loads(key_points_response["body"].read())
        key_points_text = (
            key_points_body_content.get("content", [{}])[0].get("text", "").strip()
        )

        key_points = [
            point.strip() for point in key_points_text.split("\n") if point.strip()
        ]

        return {
            "summary": summary,
            "key_points": key_points,
            "original_length": len(transcript_text.split()),
            "summary_length": len(summary.split()),
            "model_used": "anthropic.claude-3-sonnet-20240229-v1:0",
        }

    except ClientError as e:
        raise RuntimeError(f"Failed to summarize transcript: {e}")


def summarize_segments(
    segments: List[Dict[str, Any]], include_timestamps: bool = True
) -> Dict[str, Any]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    if not segments:
        return {"segment_summaries": [], "overall_summary": "", "total_segments": 0}

    segment_summaries = []

    for i, segment in enumerate(segments):
        text = segment.get("text", "")
        if not text.strip():
            segment_summaries.append(
                {"segment_index": i, "summary": "", "original_text": text}
            )
            continue

        timestamp_info = ""
        if include_timestamps and "start_time" in segment and "end_time" in segment:
            timestamp_info = f" (Timestamp: {segment['start_time']:.1f}s - {segment['end_time']:.1f}s)"

        prompt = f"""Summarize this transcript segment{timestamp_info} in one sentence:

{text}

Summary:"""

        try:
            body = json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 100,
                    "messages": [{"role": "user", "content": prompt}],
                }
            )

            response = bedrock_client.invoke_model(
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                body=body,
                contentType="application/json",
            )

            response_body = json.loads(response["body"].read())
            summary = response_body.get("content", [{}])[0].get("text", "").strip()

            segment_summaries.append(
                {
                    "segment_index": i,
                    "summary": summary,
                    "original_text": text,
                    "timestamp": f"{segment.get('start_time', 0):.1f}s - {segment.get('end_time', 0):.1f}s"
                    if include_timestamps
                    else None,
                }
            )

        except ClientError as e:
            print(f"Error summarizing segment {i}: {e}")
            segment_summaries.append(
                {
                    "segment_index": i,
                    "summary": "",
                    "original_text": text,
                    "error": str(e),
                }
            )

    all_text = " ".join([s.get("text", "") for s in segments])
    overall_summary = summarize_transcription_results(all_text, max_summary_length=150)

    return {
        "segment_summaries": segment_summaries,
        "overall_summary": overall_summary.get("summary", ""),
        "total_segments": len(segments),
        "models_used": [
            "anthropic.claude-3-haiku-20240307-v1:0",
            "anthropic.claude-3-sonnet-20240229-v1:0",
        ],
    }


def generate_meeting_minutes(
    transcript_text: str, speakers: List[str] = None
) -> Dict[str, Any]:
    bedrock_client = boto3.client(
        "bedrock-runtime",
        region_name=os.getenv("AWS_REGION", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    speakers_info = ""
    if speakers:
        speakers_info = f"Speakers present: {', '.join(speakers)}\n\n"

    prompt = f"""Generate formal meeting minutes from this transcript:

{speakers_info}{transcript_text}

Please structure the minutes with:
1. Meeting date and time (if mentioned)
2. Attendees
3. Agenda items discussed
4. Key decisions made
5. Action items with responsible parties
6. Next meeting date (if mentioned)

Meeting Minutes:"""

    try:
        body = json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            }
        )

        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-sonnet-20240229-v1:0",
            body=body,
            contentType="application/json",
        )

        response_body = json.loads(response["body"].read())
        minutes = response_body.get("content", [{}])[0].get("text", "").strip()

        return {
            "meeting_minutes": minutes,
            "transcript_length": len(transcript_text.split()),
            "minutes_length": len(minutes.split()),
            "model_used": "anthropic.claude-3-sonnet-20240229-v1:0",
        }

    except ClientError as e:
        raise RuntimeError(f"Failed to generate meeting minutes: {e}")
