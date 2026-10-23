import os
import json
from typing import List, Dict, Any
from openai import OpenAI


def record_summary(
    documents: List[Dict[str, Any]], summary_length: str = "brief"
) -> str:
    """
    Summarize retrieved document records using OpenAI GPT.

    Args:
        documents: List of document records to summarize
        summary_length: Length of summary - "brief", "detailed", or "comprehensive"

    Returns:
        str: Summary text
    """
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),
        base_url=os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )

    # Prepare document text for summarization
    document_texts = []
    for i, doc in enumerate(
        documents[:10]
    ):  # Limit to 10 documents for token constraints
        doc_str = json.dumps(doc, ensure_ascii=False)[:1000]  # Truncate long documents
        document_texts.append(f"Document {i + 1}: {doc_str}")

    combined_text = "\n\n".join(document_texts)

    # Determine summary length prompt
    length_prompts = {
        "brief": "Provide a brief 2-3 sentence summary",
        "detailed": "Provide a detailed paragraph summary",
        "comprehensive": "Provide a comprehensive multi-paragraph summary",
    }
    length_prompt = length_prompts.get(summary_length, "Provide a summary")

    prompt = f"""You are a document analysis assistant. Below are {len(documents)} document records in JSON format.

{combined_text}

{length_prompt} of these documents, highlighting key patterns, common fields, and notable data points."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful document analysis assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        summary = response.choices[0].message.content
        return summary.strip()

    except Exception as e:
        raise Exception(f"OpenAI summarization failed: {str(e)}")
