import os
import google.generativeai as genai # Provider-identifying signal
from translation_models import QualitySummaryRequest, QualitySummaryResponse

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def summarize_quality_issues(request: QualitySummaryRequest) -> QualitySummaryResponse:
    model = genai.GenerativeModel('gemini-pro') # Concrete model identifier
    prompt = f"""
    Review the following source text and its translation. Identify any quality issues such as grammatical errors, unnatural phrasing, mistranslations, or formatting problems. Provide a summary of the overall quality and a list of specific issues.

    Source Language: {request.target_language}
    Source Text: """{request.source_text}"""

    Translated Text: """{request.translated_text}"""

    Please provide the output in the following format:
    Summary: <overall summary>
    Issues: - <issue 1>
            - <issue 2>
            ...
    """
    response = model.generate_content(prompt)
    
    summary_text = response.text
    summary_lines = summary_text.split('\n')
    
    summary = ""
    issues = []
    
    in_issues_section = False
    for line in summary_lines:
        if line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Issues:"):
            in_issues_section = True
        elif in_issues_section and line.startswith("- "):
            issues.append(line.replace("- ", "").strip())
        elif in_issues_section:
            issues.append(line.strip())
            
    return QualitySummaryResponse(summary=summary, issues=issues)
