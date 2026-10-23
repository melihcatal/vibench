from typing import Dict, Any
import os
import json
from anthropic import Anthropic
from vision_models import VisualAnalysisSummary, Label, DetectedText, SafetyCategory

class AnthropicImageSummarizer:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = "claude-3-sonnet-20240229"

    def summarize_analysis(self, analysis_data: Dict[str, Any]) -> str:
        labels = analysis_data.get("labels", [])
        texts = analysis_data.get("texts", [])
        description = analysis_data.get("description", "")
        safety_categories = analysis_data.get("safety_categories", [])

        prompt = f"""Summarize the following visual analysis results into a concise, coherent summary:

Image Description:
{description}

Detected Labels:
{', '.join([label['name'] for label in labels])}

Detected Text:
{', '.join([text['text'] for text in texts])}

Safety Categories:
{', '.join([f"{cat['name']} (severity: {cat['severity']})" for cat in safety_categories])}

Provide a summary that integrates all these aspects."""

        response = self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        return response.content[0].text

def summarize_image_analysis(
    labels: List[Label], 
    texts: List[DetectedText], 
    description: str, 
    safety_categories: List[SafetyCategory]
) -> str:
    analysis_data = {
        "labels": [{"name": label.name, "confidence": label.confidence} for label in labels],
        "texts": [{"text": text.text, "confidence": text.confidence} for text in texts],
        "description": description,
        "safety_categories": [{"name": cat.name, "severity": cat.severity} for cat in safety_categories]
    }

    summarizer = AnthropicImageSummarizer()
    return summarizer.summarize_analysis(analysis_data)