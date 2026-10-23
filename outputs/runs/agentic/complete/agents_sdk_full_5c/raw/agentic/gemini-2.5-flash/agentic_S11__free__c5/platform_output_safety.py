import vertexai
from vertexai.preview.generative_models import GenerativeModel, HarmCategory, HarmBlockThreshold, SafetySetting

def check_platform_output_safety(project_id: str, location: str, model_name: str, text: str) -> dict:
    """Checks platform model output for unsafe content using Google Cloud Vertex AI safety features."""
    vertexai.init(project=project_id, location=location)
    # Using a GenerativeModel to 'evaluate' safety, though the primary safety check
    # happens during content generation. Here we can simulate a check or re-evaluate.
    # For a direct check on arbitrary text, you'd typically use specialized APIs
    # like the Perspective API or leverage the model's inherent safety filtering.
    
    # This example demonstrates how safety settings would be applied during generation
    # and how one might inspect the results. If the goal is to check an already generated
    # text *post-hoc* without regenerating, a dedicated safety API would be better.
    # For demonstration purposes using Vertex AI's GenerativeModel, we simulate an evaluation
    # by generating a response with the text and observing safety ratings.
    
    # A more direct safety check on arbitrary text would typically involve
    # a service like Google Cloud's Perspective API or calling a specific safety endpoint.
    # Since the prompt emphasizes "platform model output", we'll use Vertex AI's
    # integrated safety features.

    # We can't directly "check" an arbitrary string for safety ratings with
    # GenerativeModel.generate_content without a prompt context.
    # A workaround for demonstration is to use the text as part of a prompt
    # or rely on the safety ratings from the original generation.
    # If the text is the *output* from a previous generation, its safety ratings
    # should ideally be part of its metadata.

    # For a fresh safety check of *any* text using Google Cloud, one would typically
    # use the GenerativeModel itself with a relevant prompt, or other Google Cloud
    # safety APIs.
    
    # Let's assume for this scenario that we are re-evaluating or getting safety
    # insights for a given 'text' as if it were a model's output being processed.
    # The most direct way to get safety ratings on *content* with Vertex AI is
    # during `generate_content`.
    
    # To demonstrate provider-specific safety, we'll configure safety settings
    # and "process" the text as if it were part of an input or an existing output
    # that needs safety classification from the platform's model.
    # The current client SDK doesn't expose a direct `check_safety(text)` method
    # for post-hoc analysis that gives a `SafetyRating` object without generation.
    # However, we can construct a response-like object or utilize other services.

    # For a pure "check" on arbitrary text, we would typically use a dedicated API.
    # Given the constraint to use "platform model output" and a "concrete external provider",
    # and the Vertex AI `GenerativeModel` is what we're using, we'll show how
    # safety ratings are *obtained* through generation.
    
    # If the `text` parameter is meant to be the *actual output* from a previous
    # `generate_content` call, and we want to *re-assess* it, it's not a direct
    # feature of the SDK to get safety ratings for an arbitrary string this way
    # without re-invoking a model or using a different API (e.g., content moderation API).
    
    # As a compromise and to fulfill the requirement of showing provider-specific safety,
    # we will use a small prompt to wrap the text and observe the safety ratings
    # of the model's internal processing of that content.
    
    model = GenerativeModel(model_name)
    # The API might block the content before generating a response if it's unsafe.
    # To get safety ratings even for blocked content, we need to adjust thresholds.
    safety_settings_for_analysis = [
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_NONE
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=HarmBlockThreshold.BLOCK_NONE
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=HarmBlockThreshold.BLOCK_NONE
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=HarmBlockThreshold.BLOCK_NONE
        ),
    ]

    # Use a dummy prompt to get the safety analysis of the input `text`
    # by including it in the prompt. This will give us safety ratings based on how
    # the model perceives the *input* content, which is a proxy for output analysis.
    # A more direct method would be a dedicated content safety API.
    # Since the task is about "platform model output safety", we assume the platform
    # handles safety checks at generation.
    
    # Let's consider a practical approach for post-generation analysis:
    # If the original generation didn't provide enough safety metadata, or if
    # this function is intended to be a *secondary* safety check using a specific
    # safety model/API, then we'd use that.
    
    # For Vertex AI, the `generate_content` response itself contains safety ratings.
    # If this function receives `text` as an *already produced output*,
    # we can't get new safety ratings for it directly without re-involving a model.
    # The `collect_platform_metadata.py` already includes safety ratings.
    
    # To fulfill this as a *separate step*, we can imagine a scenario where `text`
    # is a string that needs to be evaluated for safety *post-hoc*, possibly by
    # sending it to a model that specializes in content safety or by re-using
    # the generative model for this purpose.
    
    # Let's craft a prompt to make the model "classify" the safety of the given text.
    # This is a common pattern when a dedicated safety API is not explicitly available
    # or preferred for integration.
    
    evaluation_prompt = f"Analyze the following text for harmful content and categorize its safety:

'''{text}'''

Safety analysis:"
    
    # We generate content, primarily interested in the safety_ratings of the response.
    # Even if the generated *text* for "Safety analysis:" is not directly useful,
    # the response object's safety_ratings are what we care about regarding the *input*
    # (which includes the original `text` we want to check).
    
    response = model.generate_content(
        evaluation_prompt,
        safety_settings=safety_settings_for_analysis,
        generation_config={"max_output_tokens": 50} # Keep the analysis brief
    )

    safety_report = {
        "is_safe": True,
        "violations": []
    }

    if response.candidates:
        for rating in response.candidates[0].safety_ratings:
            # If any category has a probability higher than the desired threshold, it's unsafe.
            # Vertex AI SDK's `is_blocked` indicates if the content was blocked.
            # Here we check probabilities explicitly.
            if rating.probability > HarmBlockThreshold.BLOCK_LOW_AND_ABOVE: # Example threshold
                safety_report["is_safe"] = False
                safety_report["violations"].append({
                    "category": rating.category.name,
                    "probability": rating.probability.name
                })
    
    # Additionally, check if the response was blocked.
    if response.prompt_feedback and response.prompt_feedback.block_reason:
        safety_report["is_safe"] = False
        safety_report["violations"].append({
            "category": "PROMPT_BLOCKING",
            "reason": response.prompt_feedback.block_reason.name
        })

    return safety_report
