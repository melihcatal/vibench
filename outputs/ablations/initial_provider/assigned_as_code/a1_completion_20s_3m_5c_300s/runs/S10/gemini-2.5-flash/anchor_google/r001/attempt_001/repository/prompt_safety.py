import os

from google import genai

def check_safety(payload, config=None):
    config = config or {}
    # For prompt safety, we can simulate by calling the model with safety settings
    # and checking the filters. However, a dedicated safety API would be better.
    # For this example, we'll use the genai client to send a request with safety settings.
    
    # Note: genai.Client doesn't directly expose a `check_safety` method.
    # Safety settings are usually part of the generate_content call.
    # To demonstrate provider identification, we will still use genai.Client.

    # A more robust solution might involve sending a dummy request with stringent safety settings
    # or using a dedicated content moderation API if Google provides one separately.
    
    # For the purpose of this exercise, we will assume the safety check is integrated
    # into a hypothetical genai safety API or by analyzing the response's safety attributes.
    # We'll simulate by checking if a dummy prompt would be blocked.

    prompt_text = payload.get("text", "")
    
    # In a real scenario, you'd configure safety settings on the client or the request.
    # For now, we'll assume the model's default safety features are what we're checking against.
    
    # To make it identifiable, we instantiate genai.Client.
    with genai.Client(api_key=config.get("api_key") or os.environ["GOOGLE_API_KEY"]) as client:
        # There isn't a direct "check_safety_only" API in genai.
        # A typical approach would be to send the content to the model
        # and inspect the `prompt_feedback` or `safety_ratings` in the response.
        # For this file, we'll demonstrate the client instantiation as the provider integration.
        # If the model blocked the prompt, the response would indicate it.
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt_text,
                # You would add safety_settings here if you want to override defaults
                # safety_settings=[
                #     {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                # ]
            )
            # If prompt was blocked, response might be empty or have specific feedback
            is_safe = True
            safety_feedback = []
            if response._result and response._result.prompt_feedback and response._result.prompt_feedback.safety_ratings:
                for rating in response._result.prompt_feedback.safety_ratings:
                    if rating.blocked: # Check if the prompt itself was blocked
                        is_safe = False
                        safety_feedback.append({"category": rating.category.name, "threshold": rating.threshold.name, "blocked": True})
            
            # Also check for safety ratings in candidate responses if any
            if response.candidates:
                for candidate in response.candidates:
                    if candidate.safety_ratings:
                        for rating in candidate.safety_ratings:
                            if rating.blocked:
                                is_safe = False
                                safety_feedback.append({"category": rating.category.name, "threshold": rating.threshold.name, "blocked": True})

            return {"is_safe": is_safe, "safety_feedback": safety_feedback, "model_output": response.text}

        except Exception as e:
            # If the API call itself fails due to safety concerns or other reasons
            return {"is_safe": False, "safety_feedback": [{"error": str(e)}], "model_output": ""}
