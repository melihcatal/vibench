from google.cloud import language_v1
from google.cloud.language_v1 import types
from google.cloud.language_v1 import enums

def embed_audit_note(text_content: str) -> list[float]:
    """
    Embeds a crypto audit note using Google Cloud Natural Language API for sentiment analysis
    and entity extraction as a proxy for 'embedding' for semantic search.
    Note: For direct semantic embeddings, a dedicated embedding model (e.g., from Vertex AI)
    would be more appropriate. This uses NL API for a rich text analysis that can feed into
    a search index.
    """
    client = language_v1.LanguageServiceClient()

    document = types.Document(
        content=text_content,
        type_=enums.Document.Type.PLAIN_TEXT
    )

    # Perform sentiment analysis
    sentiment = client.analyze_sentiment(request={"document": document})
    
    # Perform entity extraction
    entities_response = client.analyze_entities(request={"document": document})
    
    # As a proxy for embedding for semantic search, we can combine scores or features.
    # For a real embedding, you'd call a dedicated embedding model API.
    # This example returns a simple list of floats derived from sentiment and salient entity scores.
    embedding_proxy = [
        sentiment.document_sentiment.score,
        sentiment.document_sentiment.magnitude,
    ]

    for entity in entities_response.entities:
        # Add salience score of entities as part of the "embedding"
        embedding_proxy.append(entity.salience)
        # Limit to a reasonable number of entities to keep the vector size manageable
        if len(embedding_proxy) > 10: 
            break
            
    return embedding_proxy
