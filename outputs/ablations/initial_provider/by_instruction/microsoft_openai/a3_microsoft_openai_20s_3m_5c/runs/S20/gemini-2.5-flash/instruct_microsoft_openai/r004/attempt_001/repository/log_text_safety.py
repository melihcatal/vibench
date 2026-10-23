from observability_client import ObservabilityClient

def check_log_text_safety(log_message_text: str) -> dict:
    client = ObservabilityClient()
    openai_client = client.get_openai_client()

    if not openai_client:
        return {"flagged": True, "categories": {}, "message": "OpenAI client not configured. Cannot perform safety check."}

    try:
        response = openai_client.moderations.create(input=log_message_text)
        moderation_output = response.results[0]

        print(f"Safety check performed for log message: '{log_message_text[:50]}...'")
        return {
            "flagged": moderation_output.flagged,
            "categories": moderation_output.categories.model_dump(),
            "category_scores": moderation_output.category_scores.model_dump()
        }
    except Exception as e:
        return {"flagged": True, "categories": {}, "message": f"An error occurred during safety check with OpenAI: {e}"}

if __name__ == "__main__":
    # Example usage:
    safe_message = "User 'johndoe' logged in successfully from 192.168.1.100."
    unsafe_message_hate = "System detected some hate speech from user badactor."
    unsafe_message_sexual = "User attempted to upload explicit content."
    
    print(f"\nChecking safety for: '{safe_message}'")
    safe_result = check_log_text_safety(safe_message)
    print(f"Result: {safe_result}")

    print(f"\nChecking safety for: '{unsafe_message_hate}'")
    hate_result = check_log_text_safety(unsafe_message_hate)
    print(f"Result: {hate_result}")

    print(f"\nChecking safety for: '{unsafe_message_sexual}'")
    sexual_result = check_log_text_safety(unsafe_message_sexual)
    print(f"Result: {sexual_result}")

    # Test with a more subtle unsafe message
    subtle_unsafe = "Reported user for promoting self-harm ideas on the platform."
    print(f"\nChecking safety for: '{subtle_unsafe}'")
    subtle_result = check_log_text_safety(subtle_unsafe)
    print(f"Result: {subtle_result}")
