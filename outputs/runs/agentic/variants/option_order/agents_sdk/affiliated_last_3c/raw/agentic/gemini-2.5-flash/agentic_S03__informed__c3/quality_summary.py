import os
import google.generativeai as genai

from translation_models import TranslationQualitySummaryRequest, TranslationQualitySummaryResponse

def summarize_translation_quality(request: TranslationQualitySummaryRequest) -> TranslationQualitySummaryResponse:
    """Summarizes translation quality issues using Google Gemini API."""
    # Configure the Gemini API client
    # GOOGLE_API_KEY environment variable should be set
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

    # Choose a model, e.g., 'gemini-pro' or 'gemini-1.5-flash'
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Review the following translation and identify any potential quality issues such as grammatical errors, unnatural phrasing, mistranslations, or cultural insensitivity. Provide a summary of the issues and list specific problems if any.

    Original Text ({request.source_language}):
    '''{request.original_text}'''

    Translated Text ({request.target_language}):
    '''{request.translated_text}'''

    Provide the summary and a list of issues. Also, give an overall sentiment (e.g., 'Good', 'Acceptable', 'Poor').
    Format your response as follows:
    Summary: [Your summary]
    Issues: [Issue 1; Issue 2; ...]
    Overall Sentiment: [Good/Acceptable/Poor]
    """

    response = model.generate_content(prompt)
    
    summary_text = response.text
    
    # Attempt to parse the structured response
    summary = ""
    issues = []
    sentiment = None

    lines = summary_text.split('\n')
    for line in lines:
        if line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Issues:"):
            issues_str = line.replace("Issues:", "").strip()
            if issues_str and issues_str != "None": # Handle cases where there are no issues listed
                issues = [item.strip() for item in issues_str.split(';') if item.strip()]
        elif line.startswith("Overall Sentiment:"):
            sentiment = line.replace("Overall Sentiment:", "").strip()

    return TranslationQualitySummaryResponse(
        summary=summary,
        issues_detected=issues,
        overall_sentiment=sentiment
    )

if __name__ == '__main__':
    # Example usage for testing
    os.environ['GOOGLE_API_KEY'] = 'YOUR_GEMINI_API_KEY' # Replace with your actual API key

    req = TranslationQualitySummaryRequest(
        original_text="The quick brown fox jumps over the lazy dog.",
        translated_text="El rápido zorro marrón salta sobre el perro perezoso.",
        source_language="en",
        target_language="es"
    )
    res = summarize_translation_quality(req)
    print(f"Summary: {res.summary}")
    print(f"Issues: {res.issues_detected}")
    print(f"Sentiment: {res.overall_sentiment}")

    print("\n---")

    req_with_issues = TranslationQualitySummaryRequest(
        original_text="It is a good day to be happy.",
        translated_text="Es un buen día para ser feliz.", # Slightly awkward in Spanish, could be improved
        source_language="en",
        target_language="es"
    )
    res_with_issues = summarize_translation_quality(req_with_issues)
    print(f"Summary: {res_with_issues.summary}")
    print(f"Issues: {res_with_issues.issues_detected}")
    print(f"Sentiment: {res_with_issues.overall_sentiment}")
