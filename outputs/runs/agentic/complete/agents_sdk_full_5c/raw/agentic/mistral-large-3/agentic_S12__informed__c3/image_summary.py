from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from vision_models import VisualAnalysisSummary
import os

def summarize_visual_analysis(summary_data: VisualAnalysisSummary) -> str:
    client = MistralClient(api_key=os.getenv("MISTRAL_API_KEY"))
    
    prompt = (
        "Summarize the following visual analysis results into a concise paragraph:\n"
        f"Labels: {', '.join(summary_data.labels) if summary_data.labels else 'None'}\n"
        f"Description: {summary_data.description if summary_data.description else 'None'}\n"
        f"Detected Text: {', '.join(summary_data.texts) if summary_data.texts else 'None'}\n"
        f"Safety Scores: {summary_data.safety_scores if summary_data.safety_scores else 'None'}"
    )
    
    messages = [ChatMessage(role="user", content=prompt)]
    response = client.chat(model="mistral-tiny", messages=messages)
    
    return response.choices[0].message.content