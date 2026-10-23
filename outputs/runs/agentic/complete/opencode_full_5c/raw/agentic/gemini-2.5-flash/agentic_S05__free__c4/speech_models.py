from google.cloud import speech_v1p1beta1 as speech


def normalize_transcript_result(result: speech.StreamingRecognitionResult):
    """Normalizes a Google Cloud Speech-to-Text streaming recognition result."""
    if not result.alternatives:
        return {"transcript": "", "is_final": result.is_final, "confidence": 0.0}

    top_alternative = result.alternatives[0]
    return {
        "transcript": top_alternative.transcript,
        "is_final": result.is_final,
        "confidence": top_alternative.confidence,
    }


def create_streaming_recognize_request(
    audio_content: bytes,
) -> speech.StreamingRecognizeRequest:
    """Creates a StreamingRecognizeRequest with audio content."""
    return speech.StreamingRecognizeRequest(audio_content=audio_content)
