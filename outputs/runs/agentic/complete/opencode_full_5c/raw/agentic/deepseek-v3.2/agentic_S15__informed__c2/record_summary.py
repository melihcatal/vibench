import os
import json
from typing import Dict, Any, List, Optional
import anthropic


def summarize_records(
    documents: List[Dict[str, Any]],
    summary_length: str = "medium",
    include_fields: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Summarize retrieved document records using Anthropic Claude.

    Args:
        documents: List of document records to summarize
        summary_length: Length of summary ("short", "medium", "detailed")
        include_fields: Specific fields to include in summary

    Returns:
        dict: Summary result
    """
    try:
        # Anthropic API key from environment variable
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=api_key)

        # Prepare document text for summarization
        doc_texts = []
        for i, doc in enumerate(
            documents[:10]
        ):  # Limit to 10 documents for token constraints
            doc_str = f"Document {i + 1}:\n"

            if include_fields:
                for field in include_fields:
                    if field in doc:
                        doc_str += f"  {field}: {doc[field]}\n"
            else:
                # Include all fields except internal ones
                for key, value in doc.items():
                    if not key.startswith("_") and not isinstance(value, (dict, list)):
                        doc_str += f"  {key}: {value}\n"

            doc_texts.append(doc_str)

        documents_text = "\n".join(doc_texts)

        # Determine summary length tokens
        if summary_length == "short":
            max_tokens = 150
        elif summary_length == "detailed":
            max_tokens = 500
        else:  # medium
            max_tokens = 300

        # Create prompt for Claude
        prompt = f"""You are summarizing a set of database records. 
        Please provide a concise summary of the following {len(documents)} documents.
        
        Documents:
        {documents_text}
        
        Provide a {summary_length} summary that captures the key patterns, common fields, 
        and notable information across these documents."""

        # Call Anthropic Claude API
        # Using Claude 3 Sonnet model
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = response.content[0].text

        return {
            "success": True,
            "summary": summary,
            "document_count": len(documents),
            "summary_length": summary_length,
            "model_used": "claude-3-sonnet-20240229",
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        }

    except anthropic.APIError as e:
        return {
            "success": False,
            "error": f"Anthropic API error: {str(e)}",
            "document_count": len(documents),
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "document_count": len(documents),
        }


def summarize_single_document(
    document: Dict[str, Any], focus_fields: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Summarize a single document record.

    Args:
        document: Single document to summarize
        focus_fields: Specific fields to focus on

    Returns:
        dict: Summary result
    """
    try:
        # Anthropic API key from environment variable
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable not set")

        # Initialize Anthropic client
        client = anthropic.Anthropic(api_key=api_key)

        # Prepare document text
        doc_text = "Document content:\n"

        if focus_fields:
            for field in focus_fields:
                if field in document:
                    doc_text += f"  {field}: {document[field]}\n"
        else:
            # Include all fields except internal ones
            for key, value in document.items():
                if not key.startswith("_") and not isinstance(value, (dict, list)):
                    doc_text += f"  {key}: {value}\n"

        # Create prompt for Claude
        prompt = f"""Please provide a concise summary of this database record.
        
        {doc_text}
        
        Focus on the key information and what this record represents."""

        # Call Anthropic Claude API
        response = client.messages.create(
            model="claude-3-haiku-20240307",  # Using Haiku for faster, cheaper single doc summary
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )

        summary = response.content[0].text

        return {
            "success": True,
            "summary": summary,
            "document_id": document.get("_id", "unknown"),
            "model_used": "claude-3-haiku-20240307",
            "tokens_used": response.usage.input_tokens + response.usage.output_tokens,
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Error summarizing document: {str(e)}",
            "document_id": document.get("_id", "unknown"),
        }
