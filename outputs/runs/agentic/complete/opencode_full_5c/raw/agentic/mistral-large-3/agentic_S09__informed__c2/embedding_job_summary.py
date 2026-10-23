from typing import List, Dict, Any
import json


def summarize_embedding_job(
    job_id: str, embeddings: List[List[float]], texts: List[str]
) -> Dict[str, Any]:
    """
    Summarize embedding job results using Qwen via DashScope.
    Requires DASHSCOPE_API_KEY environment variable.
    """
    import dashscope
    from dashscope import Generation
    from http import HTTPStatus

    dashscope.api_key = dashscope.api_key or os.getenv("DASHSCOPE_API_KEY")
    if not dashscope.api_key:
        raise ValueError("DASHSCOPE_API_KEY environment variable not set")

    prompt = f"""
    Summarize the following embedding job results:
    Job ID: {job_id}
    Number of texts: {len(texts)}
    Number of embeddings: {len(embeddings)}
    
    Provide a concise summary including:
    - Total number of embeddings generated
    - Average embedding vector length
    - Any notable patterns or observations
    
    Text samples (first 3):
    {json.dumps(texts[:3], indent=2)}
    """

    response = Generation.call(model="qwen-turbo", prompt=prompt, seed=42)

    if response.status_code == HTTPStatus.OK:
        return {
            "job_id": job_id,
            "summary": response.output["text"],
            "embedding_count": len(embeddings),
            "text_count": len(texts),
        }
    else:
        raise Exception(f"DashScope Qwen API error: {response.message}")
