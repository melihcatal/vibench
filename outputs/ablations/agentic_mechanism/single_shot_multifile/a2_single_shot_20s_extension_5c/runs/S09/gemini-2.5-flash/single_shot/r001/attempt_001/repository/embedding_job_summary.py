import os
from anthropic import Anthropic

def summarize_embedding_job_results(job_results_text: str, model: str = "claude-3-haiku-20240307") -> str:
    """
    Summarizes text content related to embedding job results using Anthropic's Claude model.
    """
    client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    prompt = f"""You are an AI assistant tasked with summarizing technical reports. 
Given the following details about an embedding job, provide a concise summary highlighting key outcomes, potential issues, and significant patterns.

<embedding_job_details>
{job_results_text}
</embedding_job_details>

Summary:"""
    
    try:
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text
    except Exception as e:
        print(f"Error summarizing with Anthropic Claude: {e}")
        return f"Failed to generate summary: {e}"
