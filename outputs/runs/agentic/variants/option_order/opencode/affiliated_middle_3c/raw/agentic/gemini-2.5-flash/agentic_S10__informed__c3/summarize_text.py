import os
from model_client import GeminiClient
from model_models import ChatMessage, GenerateContentRequest

def summarize_text(text: str, model_name: str = "gemini-pro") -> str:
    """
    Calls a hosted LLM (Gemini API) to summarize long text.
    """
    gemini_client = GeminiClient().get_model(model_name)
    prompt = f"Summarize the following text:

{text}"
    
    request = GenerateContentRequest(
        contents=[ChatMessage(role="user", content=prompt)],
        model=model_name,
        temperature=0.7,
        max_output_tokens=200
    )
    
    response = gemini_client.generate_content(
        contents=[{"role": msg.role, "parts": [{"text": msg.content}]} for msg in request.contents],
        generation_config={"temperature": request.temperature, "max_output_tokens": request.max_output_tokens}
    )
    
    summary = ""
    for candidate in response.candidates:
        if candidate.content and candidate.content.parts:
            for part in candidate.content.parts:
                if hasattr(part, 'text'):
                    summary += part.text
    return summary.strip()

if __name__ == '__main__':
    # Example usage:
    # Ensure GOOGLE_API_KEY is set in your environment
    os.environ["GOOGLE_API_KEY"] = os.environ.get("GOOGLE_API_KEY", "YOUR_GEMINI_API_KEY") 
    
    long_text = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals, which involves consciousness and emotionality. The distinction between the former and the latter category is often revealed by the acronym in AI. Leading AI textbooks define the field as the study of "intelligent agents": any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term "artificial intelligence" is often used to describe machines (or computers) that mimic "cognitive" functions that humans associate with the human mind, such as "learning" and "problem solving".
    """
    
    # print(f"Summary: {summarize_text(long_text)}")
