import os
import openai
from dataclasses import dataclass

@dataclass
class TranslationQualitySummaryRequest:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    quality_issues: list[str]

@dataclass
class TranslationQualitySummaryResponse:
    summary: str

class QualitySummarizer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        if not self.client.api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        self.model = "gpt-4o"

    def summarize_quality_issues(self, request: TranslationQualitySummaryRequest) -> TranslationQualitySummaryResponse:
        prompt = (
            f"Original text ({request.source_language}):\n{request.original_text}\n\n"
            f"Translated text ({request.target_language}):\n{request.translated_text}\n\n"
            f"Identified quality issues: {', '.join(request.quality_issues) if request.quality_issues else 'None'}.\n\n"
            "Please provide a concise summary of the translation quality issues based on the provided information, focusing on how these issues might impact clarity, accuracy, or cultural appropriateness. Keep it under 150 words."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes translation quality reports."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7,
        )

        summary = response.choices[0].message.content.strip()
        return TranslationQualitySummaryResponse(summary=summary)
