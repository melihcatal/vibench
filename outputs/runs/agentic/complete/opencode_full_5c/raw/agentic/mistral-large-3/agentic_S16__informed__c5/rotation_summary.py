from openai import OpenAI
import os
import json


class OpenAIRotationSummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def summarize_rotation(self, secret_id: str, versions: list) -> str:
        version_history = [
            {
                "version_id": v["version_id"],
                "created_at": v["created_at"],
                "status": v.get("status", "active"),
            }
            for v in versions
        ]

        prompt = f"Summarize the rotation history for secret {secret_id} with the following versions: {json.dumps(version_history)}. "
        "Provide a concise summary of the rotation status, current version, and any anomalies."

        response = self.client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
