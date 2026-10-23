import requests
import time
import json
from speech_client import get_speech_config
from speech_models import TranscriptionJob, TranscriptionResult, Segment, Word

def poll_transcription(job: TranscriptionJob, polling_interval_seconds: int = 10) -> TranscriptionResult:
    speech_key, speech_region = get_speech_config()
    base_url = f"https://{speech_region}.api.cognitive.microsoft.com/speechtotext/v3.1"
    
    headers = {
        "Ocp-Apim-Subscription-Key": speech_key
    }

    job_url = f"{base_url}/transcriptions/{job.job_id}"

    while True:
        response = requests.get(job_url, headers=headers)
        response.raise_for_status()
        job_status = response.json()
        job.status = job_status["status"]
        job.last_action_date_time = job_status["lastActionDateTime"]

        if job.status in ["Succeeded", "Failed", "Canceled"]:
            break

        time.sleep(polling_interval_seconds)

    if job.status == "Succeeded":
        files_url = job_status["links"]["files"]
        files_response = requests.get(files_url, headers=headers)
        files_response.raise_for_status()
        files_data = files_response.json()

        transcript_url = None
        for file_info in files_data["values"]:
            if file_info["kind"] == "Transcription":
                transcript_url = file_info["links"]["content"]
                break
        
        if transcript_url:
            transcript_response = requests.get(transcript_url, headers=headers)
            transcript_response.raise_for_status()
            transcript_content = transcript_response.json()
            
            segments = []
            combined_text = ""
            for phrase in transcript_content["recognizedPhrases"]:
                words = []
                if "words" in phrase:
                    for word_data in phrase["words"]:
                        words.append(Word(
                            word=word_data["word"],
                            offset=word_data["offset"][:-1],  # Remove 'S' suffix if present
                            duration=word_data["duration"][:-1], # Remove 'S' suffix if present
                            confidence=word_data.get("confidence", 0.0)
                        ))
                segments.append(Segment(
                    id=len(segments),
                    start=phrase["offset"][:-1] if phrase["offset"].endswith('S') else phrase["offset"],
                    end=phrase["duration"][:-1] if phrase["duration"].endswith('S') else phrase["duration"],
                    text=phrase["display"],
                    words=words,
                    speaker_id=phrase.get("speaker", None) # Diarization
                ))
                combined_text += phrase["display"] + " "

            return TranscriptionResult(
                recognized_phrases=segments,
                duration=transcript_content.get("duration"),
                combined_recognized_phrases=combined_text.strip()
            )
        else:
            raise Exception("Transcription result file not found.")
    else:
        raise Exception(f"Transcription job failed with status: {job.status}")
