from typing import Dict, Any
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai.foundation_models import Model
import os


class RecordSummarizer:
    def __init__(self) -> None:
        self.api_key = os.getenv("WATSONX_API_KEY")
        self.project_id = os.getenv("WATSONX_PROJECT_ID")
        self.client = APIClient(api_key=self.api_key, project_id=self.project_id)
        self.model_id = "ibm/granite-13b-chat-v2"

    def summarize_record(self, document_data: Dict[str, Any], fields: list[str]) -> str:
        text = " ".join([str(document_data.get(field, "")) for field in fields])
        prompt = f"Summarize the following text in a concise manner: {text}"

        model = Model(self.model_id, self.client)
        response = model.generate_text(prompt=prompt, max_new_tokens=100)
        return response
