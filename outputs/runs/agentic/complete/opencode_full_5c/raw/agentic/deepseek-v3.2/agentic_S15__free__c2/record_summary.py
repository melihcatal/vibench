import os
from typing import Dict, Any, List
import openai


def summarize_records(
    documents: List[Dict[str, Any]], summary_type: str = "brief"
) -> Dict[str, Any]:
    """
    Summarize retrieved document records using OpenAI's GPT model.

    Args:
        documents: List of document records to summarize
        summary_type: Type of summary ("brief", "detailed", "key_points")

    Returns:
        dict: Summary results or error information
    """
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            organization=os.environ.get("OPENAI_ORG_ID"),
        )

        # Prepare document content for summarization
        document_texts = []
        for doc in documents:
            doc_data = doc.get("data", {})
            if isinstance(doc_data, dict):
                # Convert dict to readable text
                text_parts = []
                for key, value in doc_data.items():
                    if isinstance(value, (str, int, float, bool)):
                        text_parts.append(f"{key}: {value}")
                    elif isinstance(value, dict):
                        text_parts.append(f"{key}: [nested object]")
                    elif isinstance(value, list):
                        text_parts.append(f"{key}: list of {len(value)} items")
                document_texts.append(
                    f"Document {doc.get('id', 'unknown')}: " + "; ".join(text_parts)
                )
            else:
                document_texts.append(
                    f"Document {doc.get('id', 'unknown')}: {str(doc_data)}"
                )

        combined_text = "\n\n".join(document_texts)

        # Define summary prompt based on type
        if summary_type == "brief":
            system_prompt = "You are a helpful assistant that creates concise summaries of document records. Provide a brief overview in 2-3 sentences."
            user_prompt = (
                f"Summarize these {len(documents)} document records:\n\n{combined_text}"
            )
        elif summary_type == "detailed":
            system_prompt = "You are a detailed analyst that creates comprehensive summaries of document records. Provide key insights and patterns."
            user_prompt = f"Create a detailed summary of these {len(documents)} document records, highlighting important information and patterns:\n\n{combined_text}"
        else:  # key_points
            system_prompt = "You are an assistant that extracts key points from document records. Provide bullet points of the most important information."
            user_prompt = f"Extract key points from these {len(documents)} document records as bullet points:\n\n{combined_text}"

        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=500,
            temperature=0.7,
        )

        summary = response.choices[0].message.content

        return {
            "success": True,
            "summary": summary,
            "summary_type": summary_type,
            "document_count": len(documents),
            "model_used": "gpt-3.5-turbo",
            "tokens_used": response.usage.total_tokens if response.usage else None,
        }

    except openai.OpenAIError as e:
        return {
            "success": False,
            "error": f"OpenAI API error: {str(e)}",
            "error_type": type(e).__name__,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def summarize_single_document(document: Dict[str, Any]) -> Dict[str, Any]:
    """
    Summarize a single document record.

    Args:
        document: Single document record to summarize

    Returns:
        dict: Summary results
    """
    return summarize_records([document], summary_type="brief")


def extract_key_entities(documents: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Extract key entities (names, dates, locations) from document records using OpenAI.

    Args:
        documents: List of document records

    Returns:
        dict: Extracted entities
    """
    try:
        # Initialize OpenAI client
        client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            organization=os.environ.get("OPENAI_ORG_ID"),
        )

        # Prepare document content
        document_texts = []
        for doc in documents:
            doc_data = doc.get("data", {})
            if isinstance(doc_data, dict):
                text_parts = [
                    f"{key}: {value}"
                    for key, value in doc_data.items()
                    if isinstance(value, (str, int, float, bool))
                ]
                document_texts.append("; ".join(text_parts))
            else:
                document_texts.append(str(doc_data))

        combined_text = "\n".join(document_texts)

        # Call OpenAI for entity extraction
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an entity extraction assistant. Extract key entities (people, organizations, locations, dates, products) from the provided text. Return as a JSON object with entity categories.",
                },
                {
                    "role": "user",
                    "content": f"Extract entities from this text:\n\n{combined_text}",
                },
            ],
            max_tokens=300,
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        entities_text = response.choices[0].message.content
        import json

        entities = json.loads(entities_text)

        return {
            "success": True,
            "entities": entities,
            "document_count": len(documents),
            "model_used": "gpt-3.5-turbo",
        }

    except (openai.OpenAIError, json.JSONDecodeError) as e:
        return {"success": False, "error": str(e), "error_type": type(e).__name__}
    except Exception as e:
        return {"success": False, "error": str(e)}
