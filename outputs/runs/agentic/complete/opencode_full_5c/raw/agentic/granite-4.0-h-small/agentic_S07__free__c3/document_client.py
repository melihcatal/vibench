# [HELPER] document_client.py

import os

# Load configuration (you can replace this with env vars or a config file)
API_KEY = os.getenv("OPENAI_API_KEY")
assert API_KEY, "Set OPENAI_API_KEY environment variable"


# Simple client helper – mirrors the provider SDK for OCR‑Layout tasks
class DocumentClient:
    """Local wrapper around OpenAI Vision for OCR & layout extraction."""

    def __init__(self):
        self.client = openai

    def extract_text(self, image_path: str) -> str:
        return (
            self.client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "image_url": {
                                    "url": image_path,
                                },
                            }
                        ],
                        "description": "Extract plain text.",
                    }
                ],
            )
            .choices[0]
            .message.content
        )

    def extract_layout(self, image_path: str) -> str:
        return (
            self.client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "image_url": {
                                    "url": image_path,
                                },
                            }
                        ],
                        "description": "Extract layout elements.",
                    }
                ],
            )
            .choices[0]
            .message.content
        )

    def extract_tables(self, image_path: str) -> str:
        return (
            self.client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "image_url": {
                                    "url": image_path,
                                },
                            }
                        ],
                        "description": "Extract table structure.",
                    }
                ],
            )
            .choices[0]
            .message.content
        )

    def extract_key_values(self, image_path: str) -> str:
        return (
            self.client.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "image_url": {
                                    "url": image_path,
                                },
                            }
                        ],
                        "description": "Extract key‑value pairs.",
                    }
                ],
            )
            .choices[0]
            .message.content
        )
