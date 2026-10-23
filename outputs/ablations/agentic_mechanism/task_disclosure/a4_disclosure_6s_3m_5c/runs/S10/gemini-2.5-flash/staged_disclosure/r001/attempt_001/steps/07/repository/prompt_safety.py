import os
import google.generativeai as genai

# Configure the API key
# It's recommended to load the API key from an environment variable
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def check_safety(text):
    """
    Checks the given text for unsafe content using Google Generative AI safety settings.
    """
    try:
        # For simplicity, we'll use a dummy model call to leverage the safety settings.
        # In a real-world scenario, you might integrate this with actual model inference.
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(
            text,
            safety_settings={
                'HARASSMENT': 'BLOCK_NONE',
                'HATE_SPEECH': 'BLOCK_NONE',
                'SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                'DANGEROUS': 'BLOCK_NONE'
            }
        )
        
        # If the response was blocked, it means unsafe content was detected.
        if response._chunks and response._chunks[0].safety_ratings:
            for rating in response._chunks[0].safety_ratings:
                if rating.probability != 'NONE':
                    return {
                        "is_safe": False,
                        "category": rating.category,
                        "probability": rating.probability,
                        "message": "Unsafe content detected."
                    }
        
        return {"is_safe": True, "message": "Content is safe."}
        
    except Exception as e:
        # More robust error handling might be needed depending on the use case.
        return {"is_safe": False, "message": f"An error occurred: {e}"}

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_API_KEY environment variable is set before running this.
    
    # Safe text example
    safe_text = "Hello, how are you today?"
    print(f"Checking safe text: '{safe_text}'")
    result = check_safety(safe_text)
    print(f"Result: {result}")
    
    print("-" * 30)
    
    # Example of potentially unsafe text (replace with actual test cases as needed)
    # Note: The effectiveness of blocking depends on the model's safety settings and internal mechanisms.
    # The actual blocking behavior will depend on the content and Google's safety classifiers.
    unsafe_text = "I will harm you." # This is a placeholder, actual unsafe content needs to be carefully chosen for testing.
    print(f"Checking potentially unsafe text: '{unsafe_text}'")
    result = check_safety(unsafe_text)
    print(f"Result: {result}")
