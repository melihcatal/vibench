from google.cloud import speech_v1p1beta1 as speech
from typing import Generator

from speech_client import get_speech_client
from speech_models import (
    StreamingRecognitionResponse,
    SpeechRecognitionResult,
    SpeechRecognitionAlternative,
)


def process_streaming_responses(
    responses: Generator[speech.StreamingRecognizeResponse, None, None],
):
    """
    Processes streaming recognition responses from Google Cloud Speech-to-Text,
    handling partial and final results.
    """
    for response in responses:
        if not response.results:
            continue

        # The `results` list is empty or contains only a first result with `is_final=false`.
        if not response.results[0].alternatives:
            continue

        result = response.results[0]
        alternative = result.alternatives[0]

        # Provider-identifying signal: speech.StreamingRecognizeResponse
        if result.is_final:
            print(f"Final Transcript: {alternative.transcript}")
            # You might want to return or pass on the final transcript here
            yield SpeechRecognitionResult(
                alternatives=[
                    SpeechRecognitionAlternative(
                        transcript=alternative.transcript,
                        confidence=alternative.confidence,
                    )
                ],
                is_final=True,
                stability=result.stability,
            )
        else:
            print(f"Partial Transcript: {alternative.transcript}")
            # You might want to return or pass on the partial transcript here
            yield SpeechRecognitionResult(
                alternatives=[
                    SpeechRecognitionAlternative(
                        transcript=alternative.transcript,
                        confidence=alternative.confidence,
                    )
                ],
                is_final=False,
                stability=result.stability,
            )
