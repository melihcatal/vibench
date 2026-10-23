import os
from rev_ai import apiclient
from speech_models import DiarizedTranscriptRequest, DiarizedTranscriptResult

def diarized_transcript(audio_uri: str) -> DiarizedTranscriptResult:
    """Request speaker diarization for a recorded meeting using Rev AI."""
    client = apiclient.RevAiAPIClient(os.getenv("REV_AI_ACCESS_TOKEN"))
    request = DiarizedTranscriptRequest(audio_uri=audio_uri)

    job = client.submit_job_uri(
        request.audio_uri,
        metadata="Meeting Diarization",
        skip_diarization=False,
        speaker_channels_count=2,
    )

    job_details = client.get_job_details(job.id)
    if job_details.status.name == "TRANSCRIBED":
        transcript = client.get_transcript_text(job.id)
        speakers = client.get_transcript_json(job.id).get("monologues", [])
        return DiarizedTranscriptResult(
            status="COMPLETED",
            transcript=transcript,
            speakers=[
                {"speaker": mono["speaker"], "elements": mono["elements"]}
                for mono in speakers
            ],
        )
    else:
        return DiarizedTranscriptResult(status=job_details.status.name, transcript=None, speakers=[])