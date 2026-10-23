from openai import OpenAI
import json
from typing import Dict, Any, List


def summarize_documents(documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Summarizes retrieved document records using OpenAI's GPT model.

    Args:
        documents: List of documents to summarize

    Returns:
        List of summarized documents with summary field
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    if not client.api_key:
        raise ValueError("OPENAI_API_KEY must be set")

    summarized_docs = []
    for doc in documents:
        prompt = f"Summarize the following document in 2-3 sentences:\n\n{json.dumps(doc, indent=2)}"

        response = client.chat.completions.create(
            model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}]
        )

        summary = response.choices[0].message.content.strip()
        summarized_doc = doc.copy()
        summarized_doc["summary"] = summary
        summarized_docs.append(summarized_doc)

    return summarized_docs
