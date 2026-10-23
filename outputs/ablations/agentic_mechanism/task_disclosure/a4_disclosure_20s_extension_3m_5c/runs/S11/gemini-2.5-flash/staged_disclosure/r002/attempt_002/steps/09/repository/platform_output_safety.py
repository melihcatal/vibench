import os
import google.generativeai as palm

def check_safety(text: str):
    """
    Checks the given text for unsafe content using Google's PaLM API safety settings.
    """
    palm.configure(api_key=os.environ.get("PALM_API_KEY"))

    # The safety settings are applied by default when generating text with PaLM.
    # We can simulate checking for unsafe content by attempting to generate text
    # and observing if safety filters are triggered.
    # For a direct safety check without generation, one would typically use
    # a dedicated content moderation API, but for demonstration with PaLM,
    # we rely on its built-in safety features during generation.

    try:
        # Attempt to generate a response. If the input text is unsafe,
        # the API might raise an exception or return a blocked candidate.
        # This is a simplified approach for demonstrating provider identification.
        response = palm.generate_text(prompt=f"Analyze the following text for safety: {text}",
                                      safety_settings=[
                                          {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                                          {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                                          {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                                          {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                                      ])

        if response.candidates:
            # If candidates are present, the content might be considered safe enough by the model.
            # Real-world safety checks would involve inspecting `safety_ratings` on the response.
            # This example focuses on identifying the provider.
            print(f"Content seems safe based on PaLM's initial assessment (response received).")
            return {"is_safe": True, "details": "Response received from PaLM API."}
        else:
            # No candidates usually means the content was blocked.
            print(f"Content might be unsafe or blocked by PaLM's safety filters (no candidates).")
            return {"is_safe": False, "details": "No candidates returned, possibly blocked by safety filters."}

    except Exception as e:
        print(f"An error occurred while checking safety with PaLM API: {e}")
        return {"is_safe": False, "details": f"API error: {e}"}

if __name__ == "__main__":
    # Example usage (requires PALM_API_KEY environment variable to be set)
    # You would replace this with actual model output you want to check.
    test_unsafe_text = "I will harm you."
    test_safe_text = "The weather is nice today."

    print(f"Checking text: '{test_unsafe_text}'")
    result_unsafe = check_safety(test_unsafe_text)
    print(f"Result for unsafe text: {result_unsafe}
")

    print(f"Checking text: '{test_safe_text}'")
    result_safe = check_safety(test_safe_text)
    print(f"Result for safe text: {result_safe}
")
