from typing import Dict, Any, List
from transformers import pipeline


def record_text_safety(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Check user-generated document fields for unsafe content using Hugging Face Transformers."""
    classifier = pipeline(
        "text-classification", model="facebook/roberta-hate-speech-dynabench-r4-target"
    )

    for doc in documents:
        if "content" in doc:
            result = classifier(doc["content"])[0]
            doc["safety"] = {"label": result["label"], "score": result["score"]}

    return documents
