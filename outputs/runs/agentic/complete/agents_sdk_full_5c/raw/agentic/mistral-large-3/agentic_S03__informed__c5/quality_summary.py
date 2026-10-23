from openai import OpenAI
from typing import List, Dict


class TranslationQualitySummarizer:
    def __init__(self):
        self.client = OpenAI(api_key=open(".openai_api_key").read().strip())

    def summarize_quality_issues(self, source_texts: List[str], translated_texts: List[str], target_lang: str) -> Dict:
        prompt = (
            f"You are a translation quality reviewer. Review the following translations from {target_lang} "
            f"and identify any quality issues such as mistranslations, omissions, or grammatical errors. "
            f"Provide a summary of issues found:\n\n"
            f"Source Texts: {source_texts}\n\n"
            f"Translated Texts: {translated_texts}\n\n"
            f"Summary:"
        )
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500,
        )
        return {
            "summary": response.choices[0].message.content.strip(),
            "issues_detected": bool(response.choices[0].message.content.strip() != "No issues found.")
        }


def summarize_translation_quality(source_texts: List[str], translated_texts: List[str], target_lang: str) -> Dict:
    summarizer = TranslationQualitySummarizer()
    return summarizer.summarize_quality_issues(source_texts, translated_texts, target_lang)