import boto3

def select_model_family(model_family: str) -> str:
    """Select a model family from the available options."""
    available_models = {
        'anthropic': 'anthropic.claude-v2',
        'amazon': 'amazon.titan-text-express-v1'
    }
    if model_family not in available_models:
        raise ValueError(f"Model family '{model_family}' not available. Available options: {', '.join(available_models.keys())}")
    return available_models[model_family]

def perform_inference(model_id: str, prompt: str) -> str:
    """Perform inference using the selected model."""
    bedrock = boto3.client('bedrock-runtime')
    response = bedrock.invoke_model(
        modelId=model_id,
        body={
            'prompt': prompt,
            'max_tokens': 50
        }
    )
    result = response['body'].read()
    return result.decode('utf-8')