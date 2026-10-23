import time
import json
import urllib.request
from typing import Dict, Any, Optional
from speech_client import SpeechClient
from speech_models import TranscriptionResult, TranscriptionStatus


def poll_transcription_job(
    job_name: str, timeout_seconds: int = 300, poll_interval: int = 10
) -> TranscriptionResult:
    client = SpeechClient()
    transcribe_client = client.get_transcribe_client()

    start_time = time.time()

    while time.time() - start_time < timeout_seconds:
        try:
            response = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )

            job = response["TranscriptionJob"]
            status = job["TranscriptionJobStatus"]

            if status in ["COMPLETED", "FAILED"]:
                result = TranscriptionResult.from_aws_response(response)

                if (
                    result.status == TranscriptionStatus.COMPLETED
                    and result.transcript_uri
                ):
                    try:
                        with urllib.request.urlopen(result.transcript_uri) as response:
                            transcript_data = json.load(response)
                            result.transcript_text = (
                                transcript_data.get("results", {})
                                .get("transcripts", [{}])[0]
                                .get("transcript", "")
                            )
                    except Exception as e:
                        print(f"Error fetching transcript: {e}")

                return result

            time.sleep(poll_interval)

        except Exception as e:
            print(f"Error polling job: {e}")
            time.sleep(poll_interval)

    raise TimeoutError(
        f"Transcription job {job_name} timed out after {timeout_seconds} seconds"
    )


def get_transcription_result(job_name: str) -> Optional[TranscriptionResult]:
    client = SpeechClient()
    transcribe_client = client.get_transcribe_client()

    try:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )

        result = TranscriptionResult.from_aws_response(response)

        if result.status == TranscriptionStatus.COMPLETED and result.transcript_uri:
            try:
                with urllib.request.urlopen(result.transcript_uri) as response:
                    transcript_data = json.load(response)
                    result.transcript_text = (
                        transcript_data.get("results", {})
                        .get("transcripts", [{}])[0]
                        .get("transcript", "")
                    )
            except Exception as e:
                print(f"Error fetching transcript: {e}")

        return result

    except Exception as e:
        print(f"Error getting transcription result: {e}")
        return None
