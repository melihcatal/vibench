import os
from typing import Dict, Any, List
import json


def record_summary(
    documents: List[Dict[str, Any]], summary_type: str = "basic"
) -> Dict[str, Any]:
    """
    Summarize retrieved document records using OpenAI's GPT models.

    Args:
        documents: List of document records
        summary_type: Type of summary ("basic", "detailed", "analytical")

    Returns:
        dict: Summary of documents
    """
    try:
        from openai import OpenAI

        # Initialize OpenAI client
        client = OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            organization=os.environ.get("OPENAI_ORG_ID"),
        )

        # Prepare document text for summarization
        document_texts = []
        for i, doc in enumerate(documents[:10]):  # Limit to first 10 documents
            doc_data = doc.get("data", {})
            doc_id = doc.get("id", f"doc_{i}")

            # Extract text fields
            text_fields = []
            for key, value in doc_data.items():
                if isinstance(value, str) and len(value) > 10:
                    text_fields.append(f"{key}: {value[:100]}...")
                elif isinstance(value, (int, float, bool)):
                    text_fields.append(f"{key}: {value}")

            if text_fields:
                document_texts.append(f"Document {doc_id}:\n" + "\n".join(text_fields))

        if not document_texts:
            return {
                "success": False,
                "error": "No text content found in documents",
                "provider": "openai",
            }

        combined_text = "\n\n".join(document_texts)

        # Create prompt based on summary type
        if summary_type == "basic":
            prompt = f"""Summarize the key information from these documents in 3-5 bullet points:

{combined_text}

Summary:"""
        elif summary_type == "detailed":
            prompt = f"""Provide a detailed summary of these documents, including:
1. Main themes or topics
2. Key data points or statistics
3. Notable patterns or trends
4. Any missing or incomplete information

Documents:
{combined_text}

Detailed Summary:"""
        else:  # analytical
            prompt = f"""Analyze these documents and provide insights:
1. What are the main categories or types of documents?
2. What patterns or correlations do you observe?
3. What are the most common values or themes?
4. What recommendations or next steps would you suggest?

Documents:
{combined_text}

Analysis:"""

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

        summary = response.choices[0].message.content.strip()

        # Extract metadata
        usage = response.usage
        model = response.model

        return {
            "success": True,
            "summary": summary,
            "summary_type": summary_type,
            "document_count": len(documents),
            "analyzed_count": min(10, len(documents)),
            "provider": "openai",
            "model": model,
            "tokens_used": {
                "prompt": usage.prompt_tokens,
                "completion": usage.completion_tokens,
                "total": usage.total_tokens,
            },
        }

    except ImportError:
        return {
            "success": False,
            "error": "OpenAI library not installed. Install with: pip install openai",
            "provider": "openai",
        }
    except Exception as e:
        error_msg = str(e)
        if "api_key" in error_msg.lower():
            return {
                "success": False,
                "error": "OpenAI API key not configured. Set OPENAI_API_KEY environment variable.",
                "provider": "openai",
            }
        return {
            "success": False,
            "error": f"OpenAI API error: {error_msg}",
            "provider": "openai",
        }
