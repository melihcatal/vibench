import os
import logging
from typing import Optional

import dashscope
from dashscope.audio.asr import Recognition, RecognitionCallback, RecognitionResult


class SpeechClient:
    """Local configuration and client helper for DashScope Real-time ASR."""

    def __init__(self):
        self.api_key = os.getenv("DASHSCOPE_API_KEY")
        if not self.api_key:
            raise ValueError("DASHSCOPE_API_KEY environment variable not set")
        dashscope.api_key = self.api_key
        self.logger = logging.getLogger(__name__)

    def get_recognition_config(
        self,
        model: str = "paraformer-realtime-v1",
        sample_rate: int = 16000,
        format: str = "pcm",
        enable_intermediate_result: bool = True,
        enable_punctuation_prediction: bool = True,
        enable_inverse_text_normalization: bool = True,
    ) -> Recognition:
        """Build DashScope recognition configuration."""
        return Recognition(
            model=model,
            format=format,
            sample_rate=sample_rate,
            enable_intermediate_result=enable_intermediate_result,
            enable_punctuation_prediction=enable_punctuation_prediction,
            enable_inverse_text_normalization=enable_inverse_text_normalization,
        )

    def get_callback(self) -> Optional[RecognitionCallback]:
        """Return DashScope-compatible callback if needed."""
        return None
