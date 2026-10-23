import boto3
import json
from translation_client import get_sagemaker_runtime_client

def translation_memory_embedding(payload, config=None):
    config = config or {}
    client = get_sagemaker_runtime_client(region_name=config.get("region"))
    endpoint_name = config.get("sagemaker_embedding_endpoint_name", "your-embedding-endpoint-name")
    
    # The input format for a SageMaker embedding endpoint can vary. 
    # This is a common format, adjust as per your model's requirement.
    input_data = {"instances": [{"text": payload["segment"]}]}
    
    response = client.invoke_endpoint(
        EndpointName=endpoint_name,
        ContentType="application/json",
        Body=json.dumps(input_data),
    )
    
    result = json.loads(response["Body"].read().decode())
    
    # The output format can also vary. Assuming 'embeddings' key in the response.
    embeddings = result.get("embeddings", result)

    return {
        "segment": payload["segment"],
        "embedding": embeddings[0] if isinstance(embeddings, list) and embeddings else embeddings,
    }