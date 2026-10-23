from observability_client import ObservabilityClient

def translate_log_message(log_message: str, target_language: str = "French"):
    client = ObservabilityClient()
    
    if not client.openai_client:
        print("Azure OpenAI client not initialized. Cannot translate log message.")
        return ""

    prompt = f"Translate the following log message into {target_language}: '{log_message}'"
    
    try:
        response = client.openai_client.chat.completions.create(
            model=client.azure_openai_deployment_name,
            messages=[
                {"role": "system", "content": "You are an AI assistant that translates log messages."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        translated_message = response.choices[0].message.content
        return translated_message
        
    except Exception as e:
        print(f"Error translating log message with Azure OpenAI: {e}")
        return f"Failed to translate log message due to error: {e}"