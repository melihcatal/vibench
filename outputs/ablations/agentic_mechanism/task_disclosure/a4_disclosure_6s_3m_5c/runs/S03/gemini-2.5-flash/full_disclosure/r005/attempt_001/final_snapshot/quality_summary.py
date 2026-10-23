
import os
from google.cloud import aiplatform
from google.api_core.client_options import ClientOptions

def summarize_translation_quality_issues(source_text: str, translated_text: str, project_id: str, location: str = "us-central1") -> str:
    """
    Summarizes translation quality issues using Google Cloud's Generative AI.

    Args:
        source_text: The original text in the source language.
        translated_text: The translated text.
        project_id: Your Google Cloud project ID.
        location: The Google Cloud region (e.g., "us-central1").

    Returns:
        A string summarizing the translation quality issues.
    """
    client_options = ClientOptions(api_endpoint=f"{location}-aiplatform.googleapis.com")
    client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)

    # Use a specific Google Cloud model for summarization/analysis
    endpoint = client.location_path(project_id, location)
    
    # The prompt should guide the model to identify quality issues
    prompt_text = f"""
    Analyze the following source text and its translation for any quality issues such as:
    - Inaccuracies or mistranslations
    - Grammatical errors
    - Stylistic inconsistencies
    - Missing content
    - Unnatural phrasing
    - Tone issues

    Source Text: "{source_text}"
    Translated Text: "{translated_text}"

    Summarize any issues found in a concise manner. If no significant issues are found, state that the translation appears to be of good quality.
    """

    instance = aiplatform.gapic.PredictInstance(
        content=prompt_text
    ).to_value()
    
    parameters = aiplatform.gapic.PredictParameters(
        temperature=0.2,
        max_output_tokens=250
    ).to_value()

    # The model ID identifies the Google Cloud provider. Using a text-bison model.
    # For newer models like `gemini-pro`, the model name might be structured differently.
    # This example uses a typical path for a PaLM 2 model.
    model_id = "text-bison@001" 
    
    response = client.predict(
        endpoint=endpoint,
        instances=[instance],
        parameters=parameters,
        model=model_id # Explicitly identifying the model
    )

    summaries = [prediction.struct_value["content"] for prediction in response.predictions]
    return summaries[0] if summaries else "Could not generate a quality summary."

if __name__ == '__main__':
    # Example usage (replace with your actual project ID and texts)
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") # Ensure this env var is set
    
    if not PROJECT_ID:
        print("Please set the GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        source_example = "The quick brown fox jumps over the lazy dog."
        translated_example = "El zorro rápido y marrón salta sobre el perro perezoso." # Good translation
        
        print("--- Example 1: Good Quality ---")
        summary1 = summarize_translation_quality_issues(source_example, translated_example, PROJECT_ID)
        print(f"Summary: {summary1}\n")

        source_example_bad = "The cat sat on the mat."
        translated_example_bad = "El gato se sentó en la alfombra." # Grammatically correct but common mistranslation of "mat" in some contexts
        
        print("--- Example 2: Potential Issue ---")
        summary2 = summarize_translation_quality_issues(source_example_bad, translated_example_bad, PROJECT_ID)
        print(f"Summary: {summary2}\n")

        source_example_missing = "This is a test sentence for translation."
        translated_example_missing = "Esta es una oración de prueba." # Missing "para traducción"
        
        print("--- Example 3: Missing Content ---")
        summary3 = summarize_translation_quality_issues(source_example_missing, translated_example_missing, PROJECT_ID)
        print(f"Summary: {summary3}\n")
