from typing import Optional, Dict, Any
import os
from google.cloud import aiplatform
from google.oauth2 import service_account
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value


def invoke_vertex_model(
    project_id: str,
    location: str,
    model_id: str,
    prompt: str,
    parameters: Optional[Dict[str, Any]] = None,
    credentials_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Invokes a Vertex AI managed model with the given prompt and parameters.
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
    return json_format.MessageToDict(response._pb)


def invoke_vertex_chat_model(
    project_id: str,
    location: str,
    model_id: str,
    messages: list,
    parameters: Optional[Dict[str, Any]] = None,
    credentials_path: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Invokes a Vertex AI managed chat model with the given messages and parameters.
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
        model_name=f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"
    )
    endpoint = model.deployed_endpoints[0]

    instance = {"messages": messages, **parameters}
    instances = [instance]

    response = endpoint.predict(instances=instances)
    return json_format.MessageToDict(response._pb)
