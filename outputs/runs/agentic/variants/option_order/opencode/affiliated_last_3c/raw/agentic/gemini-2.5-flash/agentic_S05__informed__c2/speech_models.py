# This file defines local request, response, and normalization helpers for Streaming Speech-to-Text.
# For Google Cloud Speech-to-Text, many of these are handled directly by the SDK.
# This file serves as a placeholder for potential future custom models or normalization logic.


class TranscriptionResult:
    def __init__(self, transcript, is_final):
        self.transcript = transcript
        self.is_final = is_final

    def to_dict(self):
        return {"transcript": self.transcript, "is_final": self.is_final}
