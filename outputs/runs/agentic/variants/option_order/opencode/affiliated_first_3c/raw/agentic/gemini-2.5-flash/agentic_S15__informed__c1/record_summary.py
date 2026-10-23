import os
import google.generativeai as genai
from database_models import Document, DocumentSummary
from typing import List


def summarize_records(documents: List[Document]) -> List[DocumentSummary]:
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")  # Using a concrete model identifier

    summaries = []
    for doc in documents:
        doc_content = str(doc.data)
        prompt = f"Summarize the following document content: {doc_content}"
        response = model.generate_content(prompt)
        summary_text = response.text
        summaries.append(DocumentSummary(id=doc.id, summary_text=summary_text))
    return summaries
