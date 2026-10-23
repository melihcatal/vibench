from typing import List, Dict, Any
import os
from openai import OpenAI


class TranslationQualityAnalyzer:
    """Summarize translation quality issues using OpenAI GPT-4."""

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def analyze_quality(self, source_texts: List[str], translated_texts: List[str], target_lang: str) -> Dict[str, Any]:
        """Summarize translation quality issues."""
        prompt = (
            f"Analyze the following translations from {target_lang} for quality issues:\n\n"
            f"Source texts: {source_texts}\n\n"
            f"Translated texts: {translated_texts}\n\n"
            "Provide a summary of any grammatical, semantic, or stylistic issues found."
        )
        
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "summary": response.choices[0].message.content.strip(),
            "issues_detected": len(response.choices[0].message.content.strip().split('\n')) if response.choices[0].message.content else 0
        }


def quality_summary(source_texts: List[str], translated_texts: List[str], target_lang: str) -> Dict[str, Any]:
    """Summarize translation quality issues using OpenAI GPT-4."""
    analyzer = TranslationQualityAnalyzer()
    return analyzer.analyze_quality(source_texts, translated_texts, target_lang)