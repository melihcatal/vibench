from model_client import get_model_client, AZURE_OPENAI_CHAT_DEPLOYMENT_NAME

def invoke_model(prompt: str) -> str:
    """
    Invokes a deployed model on Azure OpenAI.
    
    Args:
        prompt: The user prompt to send to the model.

    Returns:
        The model's generated text response.
    """
    client = get_model_client()
    deployment_name = AZURE_OPENAI_CHAT_DEPLOYMENT_NAME
    
    response = client.chat.completions.create(
        model=deployment_name, # e.g. "gpt-4o-mini"
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=256,
    )
    
    if response.choices:
        return response.choices[0].message.content
    return ""

