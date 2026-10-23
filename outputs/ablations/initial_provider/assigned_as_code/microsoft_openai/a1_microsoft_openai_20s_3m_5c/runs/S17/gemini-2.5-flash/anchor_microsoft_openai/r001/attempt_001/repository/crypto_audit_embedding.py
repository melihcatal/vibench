from security_client import get_text_analytics_client
from azure.ai.textanalytics import TextAnalyticsClient, TextDocumentInput

def embed_audit_note(audit_note_text):
    text_analytics_client = get_text_analytics_client()

    # The Text Analytics client does not directly provide an embedding function
    # that is suitable for general semantic search like some other services.
    # For real embedding, you'd typically use an Azure Machine Learning endpoint
    # with a text embedding model, or Azure OpenAI Embeddings.
    # For this exercise, we will simulate an embedding by using key phrases extraction
    # as a proxy for identifying important terms that could be used for search.
    # This is not a true embedding, but demonstrates interaction with Text Analytics.

    documents = [TextDocumentInput(id="1", text=audit_note_text)]
    
    # For actual embeddings, consider Azure OpenAI or custom models via Azure ML.
    # This uses key phrase extraction as a placeholder for content representation.
    response = text_analytics_client.extract_key_phrases(documents)

    key_phrases = []
    for doc in response:
        if not doc.is_error:
            key_phrases.extend(doc.key_phrases)
        else:
            print(f"Error: {doc.id} - {doc.error.code} - {doc.error.message}")

    # In a real embedding scenario, this would return a vector (list of floats).
    # Here, we return key phrases as a searchable representation.
    return {'audit_note_text': audit_note_text, 'extracted_key_phrases': key_phrases}
