import os
from observability_client import observability_client

def translate_log_message(log_message: str, target_language: str = "es") -> str:
    try:
        prompt = f"Translate the following log message to {target_language}. Provide only the translated text, without any additional explanations or formatting.\n\nLog message: {log_message}"
        
        response = observability_client.azure_openai_client.chat.completions.create(
            model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo"), # Example model
            messages=[
                {"role": "system", "content": "You are a helpful translation assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        translated_message = response.choices[0].message.content.strip()
        print(f"Original: '{log_message}'\nTranslated ({target_language}): '{translated_message}'")
        return translated_message

    except Exception as e:
        print(f"Error translating log message: {e}")
        return f"Translation failed: {e}"

# Example usage (for testing purposes)
# if __name__ == "__main__":
#     translate_log_message("User authentication failed due to invalid credentials.", "fr")
#     translate_log_message("Service startup successful.", "de")
