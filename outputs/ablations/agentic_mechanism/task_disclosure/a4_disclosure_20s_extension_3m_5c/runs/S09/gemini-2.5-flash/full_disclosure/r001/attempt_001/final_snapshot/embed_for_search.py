from google.cloud import aiplatform_v1beta1
from google.protobuf import struct_pb2

def embed_for_search(query: str, documents: list[str], project_id: str, location: str = "us-central1"):
    """
    Embeds a query and a list of documents for semantic search using Google Cloud's text-embedding-004 model.

    Args:
        query: The query string to embed.
        documents: A list of document strings to embed.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region where the model is hosted (default: "us-central1").

    Returns:
        A tuple containing two lists:
        - query_embedding: The embedding vector for the query.
        - document_embeddings: A list of embedding vectors for the documents.
    """
    client_options = {"api_endpoint": f"{location}-aiplatform.googleapis.com"}
    client = aiplatform_v1beta1.PredictionServiceClient(client_options=client_options)
    endpoint = f"projects/{project_id}/locations/{location}/publishers/google/models/text-embedding-004"

    # Embed the query
    query_instance = struct_pb2.Value()
    query_instance.struct_value.fields["text"].string_value = query
    query_instance.struct_value.fields["task_type"].string_value = "SEMANTIC_SIMILARITY"
    query_instance.struct_value.fields["title"].string_value = "" # No title for query
    query_instances = [query_instance]
    query_response = client.predict(endpoint=endpoint, instances=query_instances)
    query_embedding = list(query_response.predictions[0]["embeddings"]["values"])

    # Embed the documents
    document_instances = []
    for doc in documents:
        doc_instance = struct_pb2.Value()
        doc_instance.struct_value.fields["text"].string_value = doc
        doc_instance.struct_value.fields["task_type"].string_value = "SEMANTIC_SIMILARITY"
        doc_instance.struct_value.fields["title"].string_value = "" # No title for document
        document_instances.append(doc_instance)
    document_response = client.predict(endpoint=endpoint, instances=document_instances)
    document_embeddings = [list(pred["embeddings"]["values"]) for pred in document_response.predictions]

    return query_embedding, document_embeddings
