import os
import json
from typing import List, Dict, Any
import anthropic


def summarize_records(
    documents: List[Dict[str, Any]], summary_type: str = "brief"
) -> Dict[str, Any]:
    """
    Summarize retrieved document records using Anthropic Claude.

    Args:
        documents: List of document records
        summary_type: Type of summary ("brief", "detailed", "key_points")

    Returns:
        dict: Summary result
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    try:
        document_texts = []
        for i, doc in enumerate(documents[:10]):
            doc_str = json.dumps(doc, indent=2)
            document_texts.append(f"Document {i + 1}:\n{doc_str}")

        documents_text = "\n\n".join(document_texts)

        prompt_map = {
            "brief": "Provide a brief 2-3 sentence summary of these documents.",
            "detailed": "Provide a detailed summary of these documents, highlighting key information.",
            "key_points": "Extract key points from these documents as a bulleted list.",
        }

        summary_instruction = prompt_map.get(summary_type, prompt_map["brief"])

        system_prompt = "You are a helpful assistant that summarizes document records."

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            temperature=0.3,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"{summary_instruction}\n\nHere are the documents:\n\n{documents_text}",
                }
            ],
        )

        summary = message.content[0].text

        return {
            "success": True,
            "summary": summary,
            "summary_type": summary_type,
            "document_count": len(documents),
            "model_used": "claude-3-haiku-20240307",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


def summarize_single_document(
    document: Dict[str, Any], fields_to_summarize: List[str] = None
) -> Dict[str, Any]:
    """
    Summarize a single document with focus on specific fields.

    Args:
        document: Document to summarize
        fields_to_summarize: List of field names to focus on

    Returns:
        dict: Summary result
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = anthropic.Anthropic(api_key=api_key)

    try:
        if fields_to_summarize:
            filtered_doc = {
                k: v for k, v in document.items() if k in fields_to_summarize
            }
            doc_text = json.dumps(filtered_doc, indent=2)
            field_info = f" (focusing on fields: {', '.join(fields_to_summarize)})"
        else:
            doc_text = json.dumps(document, indent=2)
            field_info = ""

        system_prompt = "You are a helpful assistant that summarizes document content."

        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0.3,
            system=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"Please provide a concise summary of this document{field_info}:\n\n{doc_text}",
                }
            ],
        )

        summary = message.content[0].text

        return {
            "success": True,
            "summary": summary,
            "document_id": document.get("id", "unknown"),
            "fields_summarized": fields_to_summarize,
            "model_used": "claude-3-haiku-20240307",
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
