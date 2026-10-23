import os
import openai
from dotenv import load_dotenv

load_dotenv() # Load environment variables

def summarize_embedding_job(job_details: str, embedded_texts_sample: list[str]) -> str:
    """
    Summarizes the results of an embedding job using OpenAI's GPT-3.5-turbo.
    
    Args:
        job_details: A string describing the embedding job (e.g., "batch job of 1000 documents").
        embedded_texts_sample: A sample of texts that were embedded.
    
    Returns:
        A string summary of the embedding job.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    sample_text_str = "\n".join([f"- \'{text}\'" for text in embedded_texts_sample[:5]]) # Limit sample to 5 for prompt
    
    prompt = f"""
    Please summarize the following embedding job:
    Job Details: {job_details}
    
    Sample of texts that were embedded:
    {sample_text_str}
    
    Provide a concise summary of what was embedded and the context of the job.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo", # Specific model identifier
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes technical job reports."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.7
        )
        summary = response.choices[0].message.content
        return summary
    except openai.APIError as e:
        return f"Error summarizing job: {e}"

if __name__ == '__main__':
    # Example usage (requires OPENAI_API_KEY environment variable)
    # job_description = "A daily batch embedding job for product descriptions."
    # sample_texts = [
    #     "Laptop Pro X with 16GB RAM and 512GB SSD.",
    #     "Ergonomic office chair with adjustable lumbar support.",
    #     "Wireless noise-cancelling headphones, 30-hour battery.",
    #     "Smart home hub with voice control and security features.",
    #     "Organic cotton bed sheets, queen size.",
    #     "Portable Bluetooth speaker with deep bass.",
    # ]
    # summary = summarize_embedding_job(job_description, sample_texts)
    # print("Embedding Job Summary:")
    # print(summary)
    pass
