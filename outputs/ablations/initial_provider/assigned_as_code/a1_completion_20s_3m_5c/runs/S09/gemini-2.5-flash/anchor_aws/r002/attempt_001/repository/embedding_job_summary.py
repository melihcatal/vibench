from google.cloud import aiplatform

def embedding_job_summary(embedding_results, config=None):
    config = config or {}
    project_id = config.get("project_id")
    location = config.get("location", "us-central1")

    if not project_id:
        raise ValueError("Google Cloud project_id must be provided in config.")

    aiplatform.init(project=project_id, location=location)
    model = aiplatform.GenerativeModel("gemini-pro")

    summary_prompt = "Summarize the following embedding job results. Focus on key statistics, patterns, or any notable observations about the embeddings:\n\n"
    summary_prompt += json.dumps(embedding_results, indent=2)

    response = model.generate_content(summary_prompt)
    return {"summary": response.text}

import json
