import google.cloud.aiplatform_v1beta1.types as gapic_types
from google.cloud import aiplatform

def invoke_vertex_ai_model(
    project_id: str,
    location: str,
    model_id: str,
    instances: list,
    api_endpoint: str = "us-central1-aiplatform.googleapis.com",
):
    """Invokes a provider-managed model on Google Cloud Vertex AI.

    Args:
        project_id: The Google Cloud project ID.
        location: The Google Cloud region where the model is deployed (e.g., "us-central1").
        model_id: The ID of the deployed model in Vertex AI.
        instances: A list of instances to send to the model for prediction.
        api_endpoint: The API endpoint for Vertex AI (defaults to "us-central1-aiplatform.googleapis.com").

    Returns:
        The prediction response from the Vertex AI model.
    """

    client_options = {"api_endpoint": api_endpoint}
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    
    endpoint = client.endpoint_path(
        project=project_id, location=location, endpoint=model_id
    )

    # Prepare the instances for prediction.
    # The structure of the instances depends on the model.
    # For a simple text model, each instance might be a dictionary like {"prompt": "..."}
    # For demonstration, we assume a generic instance format.
    
    # Convert instances to protobuf Value objects if they are not already.
    # This is a generic way to handle different input types.
    # In a real scenario, you would tailor this to your model's expected input.
    # This example assumes `instances` is already in a format directly usable
    # by gapic_types.PredictRequest, typically list of dicts.
    
    request = gapic_types.PredictRequest(
        endpoint=endpoint,
        instances=[gapic_types.instance.Value(struct_value=gapic_types.Struct(fields={
            key: gapic_types.Value(string_value=value) for key, value in instance.items()
        })) for instance in instances],
    )

    response = client.predict(request=request)
    return response

