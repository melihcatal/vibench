# record_summary.py
"""
Later-step integration file that summarizes retrieved document records.
Uses database_models.Document to format a concise summary.
"""

from database_models import Document


def summarize_documents(documents):
    """Generate a summary for a list of Document instances.

    Args:
        documents (list[dict]): Raw DynamoDB items or Document objects.

    Returns:
        list[dict]: Each summary contains id, created_at, updated_at, and a snippet of content.
    """
    if not isinstance(documents, list):
        documents = [documents]
    summaries = []
    for doc in documents:
        if not isinstance(doc, Document):
            doc = Document.parse_obj(doc)
        summaries.append(
            {
                "id": doc.id,
                "created_at": doc.created_at,
                "updated_at": doc.updated_at,
                "snippet": str(
                    list(doc.content.keys())[:3]
                ),  # shows first three keys as snippet
            }
        )
    return summaries
