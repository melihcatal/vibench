import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

def embedding_job_summary(job_results, project_id, location="us-central1"):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-pro")

    # Assuming job_results is a list of dictionaries, e.g., [{'text': '...', 'embedding': [...]}]
    # For summarization, we'll just take a sample or concatenate some text.
    sample_texts = [result.get('text', '') for result in job_results if 'text' in result][:5] # Summarize up to 5 texts
    summary_input_text = "\n".join(sample_texts)
    
    if not summary_input_text:
        return {"summary": "No text available to summarize from job results."}

    prompt = f"Summarize the following embedding job results. Focus on the content embedded and any notable patterns:\n\n{summary_input_text}"
    
    response = model.generate_content(prompt)
    return {"summary": response.text}
