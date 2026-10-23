from observability_client import GcpObservabilityClient
from google.cloud.aiplatform_v1.types import PredictRequest
from google.protobuf.json_format import ParseDict
from google.cloud import aiplatform

def metric_summary(payload, config=None):
    config = config or {}
    project_id = config.get('gcp_project_id')
    location = config.get('gcp_location', 'us-central1') # Default to a common region
    model_id = config.get('vertex_ai_model_id', 'text-bison@001') # Example model
    endpoint_id = f"projects/{project_id}/locations/{location}/publishers/google/models/{model_id}"

    metric_data_str = str(payload.get('metric_data')) # Convert metric data to string for LLM
    prompt_text = f"Summarize the following metric data, highlighting any significant trends or anomalies: {metric_data_str}"

    # Vertex AI expects a list of instances, each instance is a dict or a protobuf message.
    # For text models, the instance often contains a 'prompt' key.
    instance = {"prompt": prompt_text}
    instances_pb = [ParseDict(instance, aiplatform.gapic.types.PredictRequest.Instance()) for instance in [instance]]
    
    predict_request = PredictRequest(endpoint=endpoint_id, instances=instances_pb)

    client = GcpObservabilityClient().vertex_ai_client

    response = client.predict(request=predict_request)

    summary = "No summary generated."
    if response.predictions:
        # The structure of predictions can vary by model. For text-bison, it's typically a string.
        # Need to convert from protobuf Value to Python native type.
        summary = response.predictions[0].struct_value.fields['content'].string_value # Access content field

    return {'summary': summary}
