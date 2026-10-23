import os
import boto3
import time
from typing import Optional, Dict, Any


def transcribe_audio_file(audio_file_path, language_code="en-US"):
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    transcribe_client = boto3.client(
        "transcribe",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    bucket_name = "tts-qa-transcripts"
    object_key = f"audio/{os.path.basename(audio_file_path)}"

    try:
        s3_client.upload_file(audio_file_path, bucket_name, object_key)
    except Exception as e:
        raise Exception(f"Failed to upload audio to S3: {str(e)}")

    job_name = f"tts_qa_{int(time.time())}"

    try:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={"MediaFileUri": f"s3://{bucket_name}/{object_key}"},
            MediaFormat="wav",
            LanguageCode=language_code,
            Settings={"ShowSpeakerLabels": False, "ChannelIdentification": False},
        )
    except Exception as e:
        raise Exception(f"Failed to start transcription job: {str(e)}")

    max_wait_time = 300
    start_time = time.time()

    while time.time() - start_time < max_wait_time:
        try:
            response = transcribe_client.get_transcription_job(
                TranscriptionJobName=job_name
            )
            status = response["TranscriptionJob"]["TranscriptionJobStatus"]

            if status == "COMPLETED":
                transcript_uri = response["TranscriptionJob"]["Transcript"][
                    "TranscriptFileUri"
                ]

                import urllib.request
                import json

                with urllib.request.urlopen(transcript_uri) as url:
                    transcript_data = json.loads(url.read().decode())

                transcript_text = transcript_data["results"]["transcripts"][0][
                    "transcript"
                ]

                return {
                    "job_name": job_name,
                    "transcript": transcript_text,
                    "confidence": transcript_data["results"].get("confidence", 0),
                    "language_code": language_code,
                    "audio_file": f"s3://{bucket_name}/{object_key}",
                }
            elif status == "FAILED":
                failure_reason = response["TranscriptionJob"].get(
                    "FailureReason", "Unknown"
                )
                raise Exception(f"Transcription job failed: {failure_reason}")

            time.sleep(5)
        except Exception as e:
            raise Exception(f"Error checking transcription job: {str(e)}")

    raise Exception("Transcription job timed out")


def transcribe_audio_bytes(audio_bytes, sample_rate=16000, language_code="en-US"):
    import tempfile

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
        import wave
        import io

        buffer = io.BytesIO(audio_bytes)
        try:
            with wave.open(buffer, "rb") as wav_in:
                with wave.open(temp_file.name, "wb") as wav_out:
                    wav_out.setnchannels(wav_in.getnchannels())
                    wav_out.setsampwidth(wav_in.getsampwidth())
                    wav_out.setframerate(wav_in.getframerate())
                    wav_out.writeframes(wav_in.readframes(wav_in.getnframes()))
        except:
            with wave.open(temp_file.name, "wb") as wav_out:
                wav_out.setnchannels(1)
                wav_out.setsampwidth(2)
                wav_out.setframerate(sample_rate)
                wav_out.writeframes(audio_bytes)

        temp_file_path = temp_file.name

    try:
        result = transcribe_audio_file(temp_file_path, language_code)
        os.unlink(temp_file_path)
        return result
    except Exception as e:
        os.unlink(temp_file_path)
        raise e


def verify_tts_output(original_text, audio_data, language_code="en-US"):
    try:
        transcript_result = transcribe_audio_bytes(
            audio_data, language_code=language_code
        )

        transcript_text = transcript_result["transcript"]
        confidence = transcript_result.get("confidence", 0)

        import difflib

        similarity = difflib.SequenceMatcher(
            None, original_text.lower(), transcript_text.lower()
        ).ratio()

        verification_passed = similarity > 0.8 and confidence > 0.7

        return {
            "verification_passed": verification_passed,
            "original_text": original_text,
            "transcribed_text": transcript_text,
            "similarity_score": similarity,
            "transcription_confidence": confidence,
            "transcript_result": transcript_result,
            "issues": []
            if verification_passed
            else [
                f"Similarity too low: {similarity:.2f}" if similarity <= 0.8 else "",
                f"Confidence too low: {confidence:.2f}" if confidence <= 0.7 else "",
            ],
        }
    except Exception as e:
        return {
            "verification_passed": False,
            "error": str(e),
            "original_text": original_text,
            "transcribed_text": None,
            "similarity_score": 0,
            "transcription_confidence": 0,
        }


def batch_verify_tts_samples(samples):
    results = []

    for sample in samples:
        try:
            verification_result = verify_tts_output(
                sample["original_text"],
                sample["audio_data"],
                sample.get("language_code", "en-US"),
            )

            results.append(
                {
                    "sample_id": sample.get("id", f"sample_{len(results)}"),
                    **verification_result,
                }
            )
        except Exception as e:
            results.append(
                {
                    "sample_id": sample.get("id", f"sample_{len(results)}"),
                    "verification_passed": False,
                    "error": str(e),
                    "original_text": sample.get("original_text", ""),
                    "transcribed_text": None,
                    "similarity_score": 0,
                    "transcription_confidence": 0,
                }
            )

    summary = {
        "total_samples": len(results),
        "passed_samples": sum(
            1 for r in results if r.get("verification_passed", False)
        ),
        "failed_samples": sum(
            1 for r in results if not r.get("verification_passed", True)
        ),
        "average_similarity": sum(r.get("similarity_score", 0) for r in results)
        / len(results)
        if results
        else 0,
        "average_confidence": sum(r.get("transcription_confidence", 0) for r in results)
        / len(results)
        if results
        else 0,
    }

    return {"results": results, "summary": summary}


def get_transcription_job_status(job_name):
    aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set"
        )

    transcribe_client = boto3.client(
        "transcribe",
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region,
    )

    try:
        response = transcribe_client.get_transcription_job(
            TranscriptionJobName=job_name
        )
        return response["TranscriptionJob"]
    except Exception as e:
        raise Exception(f"Failed to get transcription job status: {str(e)}")
