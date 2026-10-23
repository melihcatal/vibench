import os
import openai


def summarize_visual_analysis(labels, description, text_data, safety_data):
    """Summarize visual analysis results using OpenAI GPT."""
    openai.api_key = os.getenv("OPENAI_API_KEY")

    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    analysis_text = f"""
    Image Analysis Results:
    
    Detected Labels: {", ".join([label["description"] for label in labels[:5]]) if labels else "None"}
    
    Description: {description}
    
    Detected Text: {text_data.get("full_text", "No text detected")[:200]}
    
    Safety Assessment: {"Safe" if safety_data.get("is_safe", False) else "Potentially unsafe"}
    Safety Scores: {safety_data.get("safety_scores", {})}
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes image analysis results concisely.",
            },
            {
                "role": "user",
                "content": f"Please provide a concise summary of this image analysis:\n\n{analysis_text}",
            },
        ],
        max_tokens=150,
        temperature=0.7,
    )

    summary = response.choices[0].message.content.strip()
    return {"summary": summary, "model_used": "gpt-3.5-turbo", "provider": "OpenAI"}
