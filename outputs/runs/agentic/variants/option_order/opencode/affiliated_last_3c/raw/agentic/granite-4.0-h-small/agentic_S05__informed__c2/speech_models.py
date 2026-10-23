# [HELPER] speech_models.py
# Defines request, response, and normalization helpers for Streaming Speech-to-Text

# Generic response normalization template
# This module can be extended with provider-specific parsing logic
import json


class StreamingResponse:
    def __init__(self, raw):
        self.raw = raw
        self.results = None
        self.parse()

    def parse(self):
        # Placeholder: parse provider-specific response into a unified structure
        # Example for Google: self.results = [{'alternatives': [{'transcript': '...'}]}]
        pass

    def get_transcript(self, interim=False):
        # Return the best transcription string or partials
        # Example logic: concatenate interim results if interim==True
        return ""


# Provider-specific modules can subclass StreamingResponse
# Example: DeepgramResponse(StreamingResponse), AmazonTranscribeResponse(StreamingResponse)
