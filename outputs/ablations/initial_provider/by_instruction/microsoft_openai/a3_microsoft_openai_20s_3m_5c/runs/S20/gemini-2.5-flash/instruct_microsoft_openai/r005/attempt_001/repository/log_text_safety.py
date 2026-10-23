from observability_client import ObservabilityClient

def check_log_safety(log_message: str):
    client = ObservabilityClient()
    
    if not client.openai_client:
        print("Azure OpenAI client not initialized. Cannot check log safety.")
        return None

    try:
        response = client.openai_client.moderations.create(input=log_message)
        moderation_result = response.results[0]
        return moderation_result
            
    except Exception as e:
        print(f"Error checking log safety with Azure OpenAI: {e}")
        return None