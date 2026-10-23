from document_client import DocumentClient, get_project_id
from document_models import EmbeddingRequest, EmbeddingResponse
from google.cloud.aiplatform.gapic.schema import predict as gapic_predict_schema
import json

def ocr_embedding(request: EmbeddingRequest) -> EmbeddingResponse:
    project_id = get_project_id()
    doc_client_helper = DocumentClient(project_id=project_id)
    client = doc_client_helper.get_vertex_ai_text_embedding_client()

    endpoint_id = "textembedding-gecko@001" # Using a common text embedding model

    instances = []
    for text_segment in request.text_segments:
        instances.append(gapic_predict_schema.instance.TextEmbeddingPredictionInstance(content=text_segment).to_value())

    endpoint = client.endpoint_path(project_id, doc_client_helper.location, endpoint_id)

    try:
        response = client.predict(endpoint=endpoint, instances=instances)

        embeddings = []
        for prediction in response.predictions:
            # The prediction is a Value object, convert to Python dict/list
            embedding_value = json.loads(gapic_predict_schema.instance.Value.to_json(prediction))
            embeddings.append(embedding_value["embeddings"])

        return EmbeddingResponse(embeddings=embeddings)

    except Exception as e:
        print(f"Error generating embeddings: {e}")
        return EmbeddingResponse()
