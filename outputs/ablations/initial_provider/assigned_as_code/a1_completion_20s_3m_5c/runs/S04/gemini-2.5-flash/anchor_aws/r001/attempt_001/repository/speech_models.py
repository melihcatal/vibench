from typing import Dict, Any, List

def normalize_transcription_job_status(response: Dict[str, Any]) -> Dict[str, Any]:
    job = response.get("TranscriptionJob", {})
    return {
        "job_id": job.get("TranscriptionJobName"),
        "status": job.get("TranscriptionJobStatus"),
        "completion_time": job.get("CompletionTime"),
        "failure_reason": job.get("FailureReason"),
        "transcript_file_uri": job.get("Transcript", {}).get("TranscriptFileUri"),
    }

def normalize_transcript_result(transcript_content: Dict[str, Any]) -> Dict[str, Any]:
    results = transcript_content.get("results", {})
    items = results.get("items", [])
    segments = results.get("speaker_labels", {}).get("segments", [])
    
    return {
        "full_text": results.get("transcripts", [{}])[0].get("transcript"),
        "word_timestamps": [
            {
                "word": item.get("alternatives", [{}])[0].get("content"),
                "start_time": item.get("start_time"),
                "end_time": item.get("end_time"),
                "type": item.get("type")
            } for item in items if item.get("type") == "pronunciation"
        ],
        "diarization_segments": [
            {
                "start_time": segment.get("start_time"),
                "end_time": segment.get("end_time"),
                "speaker_label": segment.get("speaker_label"),
                "items": [
                    {
                        "start_time": item.get("start_time"),
                        "end_time": item.get("end_time"),
                        "speaker_label": item.get("speaker_label"),
                        "word": item.get("alternatives", [{}])[0].get("content")
                    } for item in segment.get("items", [])
                ]
            } for segment in segments
        ]
    }

def normalize_translation_result(translation_response: Dict[str, Any]) -> str:
    return translation_response.get("TranslatedText", "")

def normalize_moderation_result(comprehend_response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "sentiment": comprehend_response.get("Sentiment"),
        "sentiment_score": comprehend_response.get("SentimentScore"),
        "entities": comprehend_response.get("Entities", []),
        "pii_entities": comprehend_response.get("PiiEntities", []),
    }

def normalize_embedding_result(bedrock_response: Dict[str, Any]) -> List[float]:
    return bedrock_response.get("embedding", [])
