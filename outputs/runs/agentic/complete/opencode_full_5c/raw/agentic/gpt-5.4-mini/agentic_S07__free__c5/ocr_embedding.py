from typing import Any, Dict
from google.cloud import aiplatform


def embed_document_sections(sections: list[str]) -> Dict[str, Any]:
    endpoint = aiplatform.MatchingEngineIndexEndpoint(index_endpoint_name=os.environ['VERTEX_AI_EMBEDDING_ENDPOINT'])
    return {'provider': 'vertex_ai_matching_engine', 'sections': sections, 'endpoint': str(endpoint)}
