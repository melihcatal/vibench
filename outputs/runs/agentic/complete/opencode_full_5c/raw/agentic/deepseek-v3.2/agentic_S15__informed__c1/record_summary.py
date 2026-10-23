import os
import json
from typing import List, Dict, Any
from anthropic import Anthropic
from database_models import DocumentSummaryRequest, DocumentSummaryResponse

# Anthropic Claude configuration
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")


def summarize_records(request: DocumentSummaryRequest) -> DocumentSummaryResponse:
    """
    Summarize retrieved document records using Anthropic Claude.
    """
    if not ANTHROPIC_API_KEY:
        return DocumentSummaryResponse(
            success=False,
            summaries={},
            error="ANTHROPIC_API_KEY environment variable is required",
            timestamp=request.timestamp,
        )

    try:
        # Initialize Anthropic client
        client = Anthropic(api_key=ANTHROPIC_API_KEY)

        summaries = {}

        # Process each document
        for doc_id in request.document_ids:
            # Fetch document data (in a real implementation, this would come from the database)
            # For now, we'll create a placeholder - in practice you'd fetch from DynamoDB
            document_data = {
                "id": doc_id,
                "content": f"Document content for {doc_id}",
                "metadata": {"source": "example"},
            }

            # Prepare prompt for summarization
            summary_options = request.summary_options or {}
            max_length = summary_options.get("max_length", 100)
            focus_areas = summary_options.get("focus_areas", [])

            prompt = f"""Please provide a concise summary of the following document data.
            
Document ID: {doc_id}
Document Data: {json.dumps(document_data, indent=2)}

Summary requirements:
- Maximum length: {max_length} characters
- Focus on: {", ".join(focus_areas) if focus_areas else "key information"}
- Include main topics, key findings, and important details
- Use clear, concise language

Summary:"""

            # Call Anthropic Claude API
            response = client.messages.create(
                model=ANTHROPIC_MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract summary from response
            if response.content and len(response.content) > 0:
                summary = response.content[0].text.strip()
                summaries[doc_id] = summary
            else:
                summaries[doc_id] = "No summary generated"

        return DocumentSummaryResponse(
            success=True, summaries=summaries, timestamp=request.timestamp
        )

    except Exception as e:
        return DocumentSummaryResponse(
            success=False,
            summaries={},
            error=f"Anthropic API error: {str(e)}",
            timestamp=request.timestamp,
        )


# Alternative implementation for batch processing
def summarize_documents_batch(documents: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Summarize multiple documents in a batch using Anthropic Claude.
    """
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")

    client = Anthropic(api_key=ANTHROPIC_API_KEY)

    # Prepare batch prompt
    documents_text = "\n\n".join(
        [
            f"Document {i + 1} (ID: {doc.get('id', f'doc-{i}')}):\n{json.dumps(doc, indent=2)}"
            for i, doc in enumerate(documents)
        ]
    )

    prompt = f"""Please provide concise summaries for each of the following documents.
For each document, provide a summary of 50-100 words focusing on key information.

Documents:
{documents_text}

Please provide summaries in the format:
1. [Document ID]: [Summary]
2. [Document ID]: [Summary]
..."""

    try:
        response = client.messages.create(
            model=ANTHROPIC_MODEL,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}],
        )

        # Parse the response to extract summaries
        if response.content and len(response.content) > 0:
            response_text = response.content[0].text
            # Simple parsing - in production you'd want more robust parsing
            summaries = {}
            lines = response_text.strip().split("\n")
            for line in lines:
                if ". " in line:
                    parts = line.split(". ", 1)
                    if len(parts) == 2:
                        doc_ref = parts[0]
                        summary = parts[1]
                        # Try to extract document ID
                        if ":" in doc_ref:
                            doc_id = doc_ref.split(":")[1].strip()
                        else:
                            doc_id = doc_ref.strip()
                        summaries[doc_id] = summary

            return summaries
        else:
            return {}

    except Exception as e:
        raise Exception(f"Failed to summarize documents: {str(e)}")


# Helper function for single document summary
def summarize_single_document(document_id: str, document_data: Dict[str, Any]) -> str:
    """
    Summarize a single document.
    """
    request = DocumentSummaryRequest(
        document_ids=[document_id], summary_options={"max_length": 150}
    )

    response = summarize_records(request)

    if response.success and document_id in response.summaries:
        return response.summaries[document_id]
    else:
        return f"Failed to summarize document {document_id}: {response.error}"
