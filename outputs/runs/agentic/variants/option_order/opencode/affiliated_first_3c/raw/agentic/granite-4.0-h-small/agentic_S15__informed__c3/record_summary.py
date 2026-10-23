import json
import os
from ibm_watsonx_ai import WatsonxApi
from database_client import DatabaseClient

# Provider: watsonx.ai text chat (IBM Granite model family)
# Credentials: WATSONX_API_KEY, WATSONX_PROJECT_ID


class RecordSummary:
    """Summarize one or more retrieved document records using Granite."""

    def __init__(self):
        self.api = WatsonxApi(
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )

    def summarize(self, documents):
        # Extract a concise text from each document for summarization
        raw_text = "\n".join(doc.get("content", "") for doc in documents)
        try:
            response = self.api.chat(
                model="granite-4.0-h",
                messages=[
                    {
                        "role": "user",
                        "content": f"Summarize the following records:\n{raw_text}",
                    }
                ],
                temperature=0.2,
            )
            return {"summary": response.choices[0].message.content}
        except Exception as e:
            return {"error": str(e)}
