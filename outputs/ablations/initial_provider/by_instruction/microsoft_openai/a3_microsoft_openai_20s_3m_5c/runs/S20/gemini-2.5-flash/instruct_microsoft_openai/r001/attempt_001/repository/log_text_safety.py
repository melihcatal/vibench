import os
from observability_client import observability_client

def check_log_text_safety(log_message: str) -> dict:
    try:
        # Azure OpenAI Moderation API for content safety
        response = observability_client.azure_openai_client.moderations.create(
            input=log_message
        )
        
        moderation_result = response.results[0]
        
        print(f"Moderation results for log message: '{log_message}'")
        print(f"  Flagged: {moderation_result.flagged}")
        for category, details in moderation_result.categories.model_dump().items():
            if details:
                print(f"  Category '{category}': {details}")
        
        return moderation_result.model_dump()

    except Exception as e:
        print(f"Error checking log text safety: {e}")
        return {"error": str(e), "flagged": True} # Assume unsafe if an error occurs

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     check_log_text_safety("This is a normal log message.")
#     check_log_text_safety("This message contains harmful content like violence.")
