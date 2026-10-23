import dataclasses
from typing import Optional, List

@dataclasses.dataclass
class TranscriptAlternative:
    transcript: str
    confidence: Optional[float] = None

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[TranscriptAlternative]
    is_final: bool
    language_code: Optional[str] = None
    # Add more fields as needed, e.g., for word-level timestamps, speaker diarization

def normalize_openai_whisper_response(response) -> SpeechRecognitionResult:
    """
    Normalizes an OpenAI Whisper API response into a common SpeechRecognitionResult format.
    Note: OpenAI Whisper API is not inherently streaming for 'interim results' in the same way
    as Google/AWS. This normalization assumes a full transcription result.
    """
    if not response or not response.text:
        return SpeechRecognitionResult(alternatives=[], is_final=True, language_code="en")

    alternative = TranscriptAlternative(transcript=response.text, confidence=None)
    return SpeechRecognitionResult(alternatives=[alternative], is_final=True, language_code=response.language)

def normalize_google_speech_response(response) -> Optional[SpeechRecognitionResult]:
    """
    Normalizes a Google Cloud Speech-to-Text streaming response into a common format.
    """
    if not response.results:
        return None

    result = response.results[0]
    alternatives = [
        TranscriptAlternative(transcript=alt.transcript, confidence=alt.confidence)
        for alt in result.alternatives
    ]
    return SpeechRecognitionResult(
        alternatives=alternatives,
        is_final=result.is_final,
        language_code=result.language_code # Note: Google Cloud's result.language_code is only for the first result after language detection
    )

def normalize_aws_transcribe_response(transcript_event: dict) -> SpeechRecognitionResult:
    """
    Normalizes an AWS Transcribe streaming transcript event into a common format.
    """
    alternatives = []
    is_final = True
    language_code = None # AWS Transcribe does not typically return language_code per result event directly for streaming

    if "Transcript" in transcript_event and "Results" in transcript_event["Transcript"]:
        for result in transcript_event["Transcript"]["Results"]:
            is_final = not result.get("IsPartial", True)
            if "Alternatives" in result:
                for alt in result["Alternatives"]:
                    alternatives.append(TranscriptAlternative(transcript=alt.get("Transcript"), confidence=None))
            # Language code might be available at a higher level or inferred from the initial request

    return SpeechRecognitionResult(alternatives=alternatives, is_final=is_final, language_code=language_code)


# Example usage for normalization (demonstration)
if __name__ == "__main__":
    # Dummy Google Cloud response object
    class DummyAlternative:
        def __init__(self, transcript, confidence):
            self.transcript = transcript
            self.confidence = confidence

    class DummyResult:
        def __init__(self, alternatives, is_final, language_code):
            self.alternatives = alternatives
            self.is_final = is_final
            self.language_code = language_code

    class DummyGoogleResponse:
        def __init__(self, results):
            self.results = results

    google_dummy_response_partial = DummyGoogleResponse(
        results=[
            DummyResult(
                alternatives=[
                    DummyAlternative(transcript="hello worl", confidence=0.9)
                ],
                is_final=False,
                language_code="en-US"
            )
        ]
    )

    google_dummy_response_final = DummyGoogleResponse(
        results=[
            DummyResult(
                alternatives=[
                    DummyAlternative(transcript="hello world", confidence=0.95)
                ],
                is_final=True,
                language_code="en-US"
            )
        ]
    )

    print("Normalized Google Partial:", normalize_google_speech_response(google_dummy_response_partial))
    print("Normalized Google Final:", normalize_google_speech_response(google_dummy_response_final))

    # Dummy AWS Transcribe event dictionary
    aws_dummy_event_partial = {
        "Transcript": {
            "Results": [
                {
                    "ResultId": "123",
                    "StartTime": 0.0,
                    "EndTime": 1.0,
                    "IsPartial": True,
                    "Alternatives": [
                        {"Transcript": "this is a partial"}
                    ]
                }
            ]
        }
    }

    aws_dummy_event_final = {
        "Transcript": {
            "Results": [
                {
                    "ResultId": "124",
                    "StartTime": 1.0,
                    "EndTime": 2.5,
                    "IsPartial": False,
                    "Alternatives": [
                        {"Transcript": "this is a final transcript."}
                    ]
                }
            ]
        }
    }
    print("Normalized AWS Partial:", normalize_aws_transcribe_response(aws_dummy_event_partial))
    print("Normalized AWS Final:", normalize_aws_transcribe_response(aws_dummy_event_final))

    # Dummy OpenAI Whisper response object
    class DummyOpenAIResponse:
        def __init__(self, text, language):
            self.text = text
            self.language = language

    openai_dummy_response = DummyOpenAIResponse(text="Hello there!", language="en")
    print("Normalized OpenAI:", normalize_openai_whisper_response(openai_dummy_response))
