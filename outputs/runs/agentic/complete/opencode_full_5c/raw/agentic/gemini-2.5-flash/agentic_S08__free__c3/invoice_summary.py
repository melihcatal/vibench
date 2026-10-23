from document_models import NormalizedExpense
from google.cloud import language_v1
import os


def summarize_invoice(expense: NormalizedExpense) -> str:
    client = language_v1.LanguageServiceClient()
    text_content = f"Invoice from {expense.vendor_name or 'unknown vendor'} on {expense.transaction_date or 'unknown date'} for a total of {expense.total_amount or 'unknown'} {expense.currency or 'USD'}.\n"
    if expense.line_items:
        text_content += "Line items include: "
        text_content += ", ".join(
            [item.description or "" for item in expense.line_items]
        )

    document = language_v1.Document(
        content=text_content, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Using entity sentiment to get a sense of key entities, could be expanded for more complex summarization
    response = client.analyze_entity_sentiment(document=document)

    summary_parts = []
    for entity in response.entities:
        if (
            entity.name and entity.sentiment.score > 0.1
        ):  # Focus on positive/neutral entities
            summary_parts.append(entity.name)

    if summary_parts:
        return f"Invoice summary: Key entities identified: {', '.join(summary_parts)}. Total amount: {expense.total_amount} {expense.currency}."
    else:
        return f"Invoice from {expense.vendor_name or 'unknown'}. Total: {expense.total_amount} {expense.currency}. No specific entities highlighted."
