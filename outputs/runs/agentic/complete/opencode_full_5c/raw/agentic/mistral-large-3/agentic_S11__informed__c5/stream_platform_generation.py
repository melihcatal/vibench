from typing import Iterator, Dict, Any
import os
from google.cloud import aiplatform
from google.oauth2 import service_account
from google.protobuf import json_format


def stream_vertex_generation(
    project_id: str,
    location: str,
    model_id: str,
    prompt: str,
    parameters: Optional[Dict[str, Any]] = None,
    credentials_path: Optional[str] = None,
) -> Iterator[Dict[str, Any]]:
    """
    Streams output from a Vertex AI managed model while preserving provider response objects.
    Yields each chunk as a dictionary with the full response structure.
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

    response = endpoint.predict(instances=instances, stream=True)
    for chunk in response:
        yield json_format.MessageToDict(chunk._pb)
