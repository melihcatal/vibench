from observability_client import get_generative_model
from typing import List, Dict, Any

def log_text_safety(log_messages: List[str]) -> Dict[str, Any]:
    model = get_generative_model("gemini-pro") # Using gemini-pro for safety checks

    safety_findings = {}
    for i, message in enumerate(log_messages):
        prompt = (
            "Analyze the following log message for any unsafe content, "
            "such as personally identifiable information (PII), sensitive data, "
            "or potentially harmful instructions. Respond with 'SAFE' if no unsafe content is found, "
            "otherwise describe the unsafe content. Only respond with SAFE or the description."
            f"\n\nLog Message: {message}"
        )
        response = model.generate_content(prompt)
        safety_findings[f"log_message_{i}"] = {"message": message, "safety_check": response.text.strip()}

    return safety_findings
