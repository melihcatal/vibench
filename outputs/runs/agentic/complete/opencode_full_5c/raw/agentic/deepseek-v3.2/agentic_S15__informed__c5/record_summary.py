import os
import json
from typing import Dict, Any, List
from openai import OpenAI


def summarize_records(
    documents: List[Dict[str, Any]], summary_type: str = "brief"
) -> Dict[str, Any]:
    """
    Summarize retrieved document records using OpenAI GPT.

    Args:
        documents: List of document records to summarize
        summary_type: Type of summary ("brief", "detailed", "key_points")

    Returns:
        dict: Summary result
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY environment variable is not set",
            "summary": None,
        }

    if not documents:
        return {
            "success": True,
            "summary": "No documents to summarize",
            "document_count": 0,
        }

    client = OpenAI(api_key=api_key)

    # Prepare document text for summarization
    document_texts = []
    for i, doc in enumerate(documents[:10]):  # Limit to first 10 documents
        doc_str = json.dumps(doc, indent=2, default=str)
        document_texts.append(f"Document {i + 1}:\n{doc_str}")

    combined_text = "\n\n".join(document_texts)

    # Create prompt based on summary type
    if summary_type == "brief":
        prompt = f"Briefly summarize the key information from these {len(documents)} documents:\n\n{combined_text}"
    elif summary_type == "detailed":
        prompt = f"Provide a detailed summary of these {len(documents)} documents:\n\n{combined_text}"
    elif summary_type == "key_points":
        prompt = f"Extract the key points from these {len(documents)} documents:\n\n{combined_text}"
    else:
        prompt = f"Summarize these {len(documents)} documents:\n\n{combined_text}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes document content.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        summary = response.choices[0].message.content

        return {
            "success": True,
            "summary": summary,
            "document_count": len(documents),
            "summary_type": summary_type,
            "model": "gpt-3.5-turbo",
        }
    except Exception as e:
        return {"success": False, "error": str(e), "summary": None}


def summarize_single_document(
    document: Dict[str, Any], fields_to_summarize: List[str] = None
) -> Dict[str, Any]:
    """
    Summarize a single document focusing on specific fields.

    Args:
        document: Single document to summarize
        fields_to_summarize: List of field names to focus on

    Returns:
        dict: Summary result
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return {
            "success": False,
            "error": "OPENAI_API_KEY environment variable is not set",
            "summary": None,
        }

    client = OpenAI(api_key=api_key)

    # Filter document to specified fields
    if fields_to_summarize:
        filtered_doc = {k: v for k, v in document.items() if k in fields_to_summarize}
    else:
        filtered_doc = document

    doc_str = json.dumps(filtered_doc, indent=2, default=str)

    prompt = f"Summarize this document content:\n\n{doc_str}"

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes document content.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.3,
        )

        summary = response.choices[0].message.content

        return {
            "success": True,
            "summary": summary,
            "document_id": document.get("_id", "unknown"),
            "model": "gpt-3.5-turbo",
        }
    except Exception as e:
        return {"success": False, "error": str(e), "summary": None}
