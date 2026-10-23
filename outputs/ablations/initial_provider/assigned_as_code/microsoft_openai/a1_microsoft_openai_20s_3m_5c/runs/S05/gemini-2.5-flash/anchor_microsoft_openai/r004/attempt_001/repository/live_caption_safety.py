import google.generativeai as genai
from typing import Generator
from speech_models import SpeechRecognitionResult

def live_caption_safety(caption_results: Generator[SpeechRecognitionResult, None, None], google_api_key: str) -> Generator[dict, None, None]:
    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel('gemini-pro')

    for result in caption_results:
        if result.is_final and result.text:
            try:
                response = model.generate_content(
                    f"Analyze the following text for unsafe content: {result.text}. Respond with a JSON object indicating if the content is safe or not, and a reason if unsafe. Example: {{\"safe\": true}}" # Using a prompt for content safety analysis
                )
                # Assuming the model returns a text response that needs to be parsed as JSON
                # For a real implementation, you'd likely use a dedicated safety API or stricter parsing
                yield {"text": result.text, "safety_analysis": response.text}
            except Exception as e:
                yield {"text": result.text, "safety_analysis": {"error": str(e)}}
