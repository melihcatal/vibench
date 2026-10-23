import os
import google.generativeai as genai
from database_models import Document
from typing import List

def summarize_documents(documents: List[Document]) -> str:
    """
    Summarizes a list of document records using the Google Gemini API.
    Requires GOOGLE_API_KEY to be set in the environment.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Use the appropriate model for text generation
    model = genai.GenerativeModel('gemini-pro')

    document_texts = []
    for doc in documents:
        # Assuming a simple serialization of document data for summarization
        document_texts.append(f"Document ID: {doc.id}, Content: {doc.data}")

    combined_text = "\n".join(document_texts)
    prompt = f"Summarize the following document records:\n\n{combined_text}"

    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY env var)
    # from database_client import get_firestore_client
    # from fetch_document import fetch_document

    # Dummy documents for demonstration
    sample_docs = [
        Document("doc1", {"title": "First Report", "content": "This is the content of the first report, detailing initial findings."}),
        Document("doc2", {"title": "Second Analysis", "content": "Analysis of collected data shows a significant trend in user engagement."})
    ]
    
    # print(f"Summary: {summarize_documents(sample_docs)}")
    print("To run this example, ensure GOOGLE_API_KEY is set and uncomment the example usage.")
