import os
from openai import OpenAI
from typing import Dict, Any, List, Optional


def record_summary(
    documents: List[Dict[str, Any]],
    summary_type: str = "brief",
    language: str = "english",
) -> Dict[str, Any]:
    """
    Summarize retrieved document records using OpenAI GPT.

    Args:
        documents: List of document records to summarize
        summary_type: Type of summary ("brief", "detailed", "key_points")
        language: Language for the summary

    Returns:
        dict: Summary result
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        if not client.api_key:
            return {
                "success": False,
                "error": "OpenAI API key not found in environment variables",
                "provider": "openai",
            }

        # Prepare document content for summarization
        document_texts = []
        for i, doc in enumerate(
            documents[:10]
        ):  # Limit to 10 documents for token efficiency
            if isinstance(doc, dict):
                # Extract text content from document
                doc_str = str(doc)
                if len(doc_str) > 1000:
                    doc_str = doc_str[:1000] + "..."
                document_texts.append(f"Document {i + 1}: {doc_str}")

        if not document_texts:
            return {
                "success": False,
                "error": "No document content to summarize",
                "provider": "openai",
            }

        # Create prompt based on summary type
        if summary_type == "brief":
            prompt_instruction = "Provide a brief 2-3 sentence summary of the main themes across these documents."
        elif summary_type == "detailed":
            prompt_instruction = (
                "Provide a detailed summary covering key points from each document."
            )
        elif summary_type == "key_points":
            prompt_instruction = "Extract 5-7 key points or findings from these documents as bullet points."
        else:
            prompt_instruction = "Summarize these documents."

        # Build the complete prompt
        prompt = f"""Please analyze the following documents and {prompt_instruction}

Documents:
{chr(10).join(document_texts)}

Please provide the summary in {language}."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes document collections.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        summary = response.choices[0].message.content

        # Extract metadata from response
        usage = response.usage
        model = response.model

        # Generate statistics about the documents
        doc_count = len(documents)
        avg_field_count = sum(
            len(doc) for doc in documents if isinstance(doc, dict)
        ) / max(doc_count, 1)

        # Identify common fields
        if documents and isinstance(documents[0], dict):
            all_fields = set()
            for doc in documents:
                if isinstance(doc, dict):
                    all_fields.update(doc.keys())
            common_fields = list(all_fields)[:10]  # First 10 unique fields
        else:
            common_fields = []

        return {
            "success": True,
            "summary": summary,
            "summary_type": summary_type,
            "language": language,
            "statistics": {
                "document_count": doc_count,
                "average_fields_per_document": round(avg_field_count, 2),
                "common_fields": common_fields[:5],
            },
            "provider": "openai",
            "model": model,
            "usage": {
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
            },
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "openai",
            "model": "gpt-3.5-turbo",
        }


def summarize_single_document(
    document: Dict[str, Any], focus_fields: List[str] = None
) -> Dict[str, Any]:
    """
    Summarize a single document using OpenAI GPT.

    Args:
        document: Single document to summarize
        focus_fields: Specific fields to focus on

    Returns:
        dict: Summary result
    """
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        if not client.api_key:
            return {
                "success": False,
                "error": "OpenAI API key not found in environment variables",
                "provider": "openai",
            }

        # Prepare document content
        if focus_fields:
            # Extract only specified fields
            doc_content = {}
            for field in focus_fields:
                if field in document:
                    doc_content[field] = document[field]
        else:
            doc_content = document

        # Convert to text
        doc_text = str(doc_content)
        if len(doc_text) > 2000:
            doc_text = doc_text[:2000] + "..."

        # Create prompt
        prompt = f"""Please summarize the following document:

{document}

Provide a concise summary that captures the main information and key details."""

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that summarizes documents.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=300,
            temperature=0.2,
        )

        summary = response.choices[0].message.content

        return {
            "success": True,
            "summary": summary,
            "document_id": document.get("id", "unknown"),
            "focus_fields": focus_fields,
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "token_count": response.usage.total_tokens,
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "provider": "openai",
            "model": "gpt-3.5-turbo",
        }
