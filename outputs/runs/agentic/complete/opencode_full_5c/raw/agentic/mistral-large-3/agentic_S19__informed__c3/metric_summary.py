from typing import Dict, List, Optional
import os
from datetime import datetime, timedelta
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage


class MetricSummarizer:
    def __init__(self):
        self.client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))

    def summarize_metric_trends(self, metric_name: str, datapoints: List[Dict]) -> str:
        if not datapoints:
            return "No datapoints available for summarization."

        prompt = f"Summarize the following metric trends for {metric_name}. "
        prompt += "Highlight any anomalies, trends, or notable patterns. "
        prompt += "Provide the summary in a concise paragraph.\n\n"
        prompt += "Datapoints:\n"
        for dp in datapoints:
            prompt += f"- Timestamp: {dp.get('timestamp')}, "
            prompt += f"Average: {dp.get('average')}, "
            prompt += f"Sum: {dp.get('sum')}, "
            prompt += f"Minimum: {dp.get('minimum')}, "
            prompt += f"Maximum: {dp.get('maximum')}\n"

        messages = [ChatMessage(role="user", content=prompt)]

        response = self.client.chat(model="mistral-large-latest", messages=messages)
        return response.choices[0].message.content
