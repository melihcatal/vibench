import os
import cohere

def collect_metadata(prompt: str, model: str = "command"):
    """
    Returns model output together with provider platform metadata (Cohere).
    """
    co = cohere.Client(os.environ.get("COHERE_API_KEY"))

    response = co.generate(
        prompt=prompt,
        model=model,
        num_generations=1,
        return_likelihoods='GENERATION',
        # Additional parameters can be set as needed for metadata collection
    )

    # Cohere's response object contains metadata like generation_id, token_likelihoods, etc.
    # We'll return the text and some selected metadata.
    if response.generations:
        generation = response.generations[0]
        return {
            "text": generation.text,
            "generation_id": generation.id,
            "likelihood": generation.likelihood,
            "finish_reason": generation.finish_reason
        }
    return {"text": "", "metadata": "No generation found"}
