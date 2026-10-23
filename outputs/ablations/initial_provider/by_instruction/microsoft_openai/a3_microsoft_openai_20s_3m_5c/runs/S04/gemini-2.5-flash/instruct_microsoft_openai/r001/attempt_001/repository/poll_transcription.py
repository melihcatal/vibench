import os
import requests
import time
from speech_client import AzureSpeechClient
from speech_models import TranscriptionResponse, TranscriptSegment, DiarizationResult, WordTimestamp, TimestampedTranscript
from typing import List, Union

def poll_transcription(job_id: str) -> TranscriptionResponse:
    client = AzureSpeechClient()
    
    headers = {
        "Ocp-Apim-Subscription-Key": client.speech_key
    }
    
    # Polling the status of the transcription job
    # This URL is a placeholder and would need to be the actual Azure batch transcription endpoint
    # Documentation: https://learn.microsoft.com/en-us/azure/cognitive-services/speech-service/batch-transcription-get-results
    
    status_url = f"https://{client.service_region}.customspeech.ai/api/speechtotext/v3.1/transcriptions/{job_id}"
    
    while True:
        print(f"Polling transcription job {job_id}...")
        response = requests.get(status_url, headers=headers)
        response.raise_for_status()
        status_data = response.json()
        
        current_status = status_data.get("status")
        print(f"Current status: {current_status}")

        if current_status in ["Succeeded", "Failed", "Canceled"]:
            break
        
        time.sleep(10) # Wait for 10 seconds before polling again

    transcript_url = None
    diarization_result_url = None
    word_timestamps_url = None

    if current_status == "Succeeded":
        files_url = status_data.get("links", {}).get("files")
        if files_url:
            files_response = requests.get(files_url, headers=headers)
            files_response.raise_for_status()
            files_data = files_response.json()
            
            for file_entry in files_data.get("values", []):
                kind = file_entry.get("kind")
                if kind == "Transcription":
                    transcript_url = file_entry.get("links", {}).get("contentUrl")
                elif kind == "Diarization":
                    diarization_result_url = file_entry.get("links", {}).get("contentUrl")
                elif kind == "WordLevelTimestamps": # This might be part of the Transcription kind or a separate one depending on API version
                    word_timestamps_url = file_entry.get("links", {}).get("contentUrl")

    return TranscriptionResponse(
        job_id=job_id,
        status=current_status,
        transcript_url=transcript_url,
        diarization_result_url=diarization_result_url,
        word_timestamps_url=word_timestamps_url
    )

def get_transcript_content(content_url: str) -> Union[List[TranscriptSegment], List[WordTimestamp]]:
    response = requests.get(content_url)
    response.raise_for_status()
    content = response.json()

    if "recognizedPhrases" in content: # Typical structure for diarized/timestamped results
        segments = []
        for phrase in content["recognizedPhrases"]:
            for speaker_segment in phrase.get("speakerSegments", [phrase]): # Handle diarization if present
                segments.append(TranscriptSegment(
                    id=len(segments) + 1,
                    start=speaker_segment.get("offsetInTicks") or phrase.get("offsetInTicks"),
                    end=speaker_segment.get("durationInTicks") or phrase.get("durationInTicks"),
                    text=speaker_segment.get("text") or phrase.get("text"),
                    speaker=speaker_segment.get("speakerId")
                ))
        return segments
    elif "segments" in content: # Another possible structure
        segments = []
        for segment in content["segments"]:
            segments.append(TranscriptSegment(
                id=segment.get("id"),
                start=segment.get("start"),
                end=segment.get("end"),
                text=segment.get("text"),
                speaker=segment.get("speaker")
            ))
        return segments
    elif "words" in content: # For word-level timestamps
        words = []
        for word_data in content["words"]:
            words.append(WordTimestamp(
                word=word_data.get("word"),
                start=word_data.get("offsetInTicks"),
                end=word_data.get("durationInTicks")
            ))
        return words
    
    return content # Fallback if structure is unexpected
