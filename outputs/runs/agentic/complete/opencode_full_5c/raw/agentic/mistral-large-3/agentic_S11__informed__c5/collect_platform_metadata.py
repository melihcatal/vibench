from typing import Dict, Any, Tuple
import os
from google.cloud import aiplatform
from google.oauth2 import service_account
from google.protobuf import json_format


def collect_vertex_metadata(
    project_id: str,
    location: str,
    model_id: str,
    prompt: str,
    parameters: Optional[Dict[str, Any]] = None,
    credentials_path: Optional[str] = None,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Invokes a Vertex AI model and returns the model output together with platform metadata.
    Metadata includes usage, resource IDs, and model handles.
    """
    if parameters is None:
        parameters = {}

    if credentials_path:
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path
        )
        aiplatform.init(project=project_id, location=location, credentials=credentials)
    else:
        aiplatform.init(project=project_id, location=location)

    model = aiplatform.Model(
        model_name=f"projects/{project_id}/locations/{location}/models/{model_id}"
    )
    endpoint = model.deployed_endpoints[0]

    instance = {"prompt": prompt, **parameters}
    instances = [instance]

    response = endpoint.predict(instances=instances)
    response_dict = json_format.MessageToDict(response._pb)

    metadata = {
        "model_id": model_id,
        "model_resource_name": model.resource_name,
        "endpoint_resource_name": endpoint.resource_name,
        "project_id": project_id,
        "location": location,
        "usage": response_dict.get("metadata", {}).get("usage", {}),
    }

    return response_dict, metadata
