import google.generativeai as genai
import os

def summarize_translation_quality_issues(original_text: str, translated_text: str, target_language: str) -> str:
    """
    Summarizes potential quality issues in a translation using the Google Gemini API.
    """
    genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"""
    Review the following original text and its translation into {target_language}.
    Identify any potential quality issues such as:
    - Inaccuracies or mistranslations
    - Grammatical errors in the translation
    - Unnatural phrasing or awkward sentence structure
    - Missing or added content
    - Incorrect tone or style

    Original Text:
    '''
    {original_text}
    '''

    Translated Text ({target_language}):
    '''
    {translated_text}
    '''

    Provide a concise summary of the identified quality issues, if any.
    If the translation appears to be high quality with no significant issues, state that.
    """

    response = model.generate_content(prompt)
    return response.text
