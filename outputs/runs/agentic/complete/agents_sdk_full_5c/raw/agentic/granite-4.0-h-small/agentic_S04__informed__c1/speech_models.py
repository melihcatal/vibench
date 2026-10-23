from typing import List, Dict

class SpeechModels:
    """Local helpers for request/response normalization and client-side validation for Batch STT"""

    @staticmethod
    def normalize_transcribe_request(job_name: str, media_uri: str, language_code: str = "en-US") -> Dict:
        """Format AWS Transcribe request payload"""
        return {
            "TranscriptionJobName": job_name,
            "Media": {"MediaFileUri": media_uri},
            "LanguageCode": language_code,
            # Optional: MediaSampleRateHertz, MediaEncoding
        }

    @staticmethod
    def is_job_complete(status_json: Dict) -> bool:
        """Check if the returned job status indicates completion"""
        return status_json.get("TranscriptionJob", {}).get("TranscriptionJobStatus") in {
            "COMPLETED",
            "FAILED",
            "PARTIAL_RESULTS"
        }

    @staticmethod
    def extract_transcript(status_json: Dict) -> str:
        """Pull the transcript out of a completed job response"""
        return status_json.get("TranscriptionJob", {}) .get("Transcript", {}) .get("TranscriptFileUri")

    @staticmethod
    def extract_timestamps(status_json: Dict) -> List[Dict]:
        """If supported by provider, return word/segment timestamps"""
        # Example: Transcribe supports $results$item$alternatives$timestamps
        return status_json.get("TranscriptionJob", {}) .get("Transcript", {}) .get("Items", [])

    @staticmethod
    def validate_language_code(lang: str) -> str:
        """Basic validation against AWS-supported codes"""
        supported = {"en-US", "es-US", "en-GB", "fr-CA", "de-DE"}
        return lang if lang in supported else "en-US"
