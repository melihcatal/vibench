from google.cloud.speech_v1p1beta1 import types
from typing import Dict, Any, Optional


class StreamingRecognitionConfig:
    """Helper class for configuring streaming recognition requests."""

    def __init__(
        self,
        config: types.RecognitionConfig,
        interim_results: bool = True,
        single_utterance: bool = False,
    ):
        self.config = config
        self.interim_results = interim_results
        self.single_utterance = single_utterance

    def to_streaming_config(self) -> types.StreamingRecognitionConfig:
        return types.StreamingRecognitionConfig(
            config=self.config,
            interim_results=self.interim_results,
            single_utterance=self.single_utterance,
        )


def normalize_response(response: types.StreamingRecognizeResponse) -> Dict[str, Any]:
    """Normalizes a streaming recognition response into a structured dict."""
    results = []
    for result in response.results:
        results.append(
            {
                "transcript": result.alternatives[0].transcript,
                "is_final": result.is_final,
                "stability": result.stability,
                "alternatives": [
                    {
                        "transcript": alt.transcript,
                        "confidence": alt.confidence,
                        "words": [
                            {
                                "word": word.word,
                                "start_time": word.start_time.total_seconds(),
                                "end_time": word.end_time.total_seconds(),
                            }
                            for word in alt.words
                        ],
                    }
                    for alt in result.alternatives
                ],
            }
        )
    return {"results": results}
