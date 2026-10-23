from typing import Dict, Any, List
from transformers import pipeline


class RecordSummarizer:
    """Summarize document records using Hugging Face Transformers."""

    def __init__(self):
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    def summarize(self, text: str, max_length: int = 130) -> str:
        """Summarize text using the BART model."""
        summary = self.summarizer(
            text, max_length=max_length, min_length=30, do_sample=False
        )
        return summary[0]["summary_text"]


def record_summary(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Summarize retrieved document records."""
    summarizer = RecordSummarizer()
    summarized_docs = []

    for doc in documents:
        if "content" in doc:
            doc["summary"] = summarizer.summarize(doc["content"])
        summarized_docs.append(doc)

    return summarized_docs
