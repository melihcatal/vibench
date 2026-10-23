import json


class SpeechModel:
    """Define local request, response, and normalization helpers for Streaming Speech-to-Text."""

    @staticmethod
    def normalize_transcript(event):
        """Extracts and normalizes transcript text from a streaming event."""
        if event.get("results"):
            for result in event["results"]:
                if result.get("alternatives"):
                    txt = result["alternatives"][0].get("transcript", "")
                    return txt.strip().lower()
        return ""

    @staticmethod
    def build_request_chunk(chunk_bytes):
        """Builds a request payload for a streaming chunk (raw 16-bit PCM)."""
        # Placeholder for actual request formatting if needed
        return chunk_bytes


# Helper functions for other steps can import this module
