from typing import Dict, List
import anthropic


def record_summary(documents: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Summarize retrieved document records using Anthropic's Claude model."""
    client = anthropic.Anthropic(api_key=anthropic.Anthropic().api_key)
    summaries = []

    for doc in documents:
        prompt = f"Summarize the following document in 2-3 sentences:\n\n{doc['body']}"
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=100,
            messages=[{"role": "user", "content": prompt}],
        )
        summaries.append(
            {"document_id": doc["id"], "summary": response.content[0].text}
        )

    return summaries
