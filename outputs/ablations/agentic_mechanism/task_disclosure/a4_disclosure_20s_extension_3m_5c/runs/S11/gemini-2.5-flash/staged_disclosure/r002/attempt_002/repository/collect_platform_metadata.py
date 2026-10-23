import os
import openai

def get_model_output_with_metadata(prompt: str):
    """
    Returns model output together with provider platform metadata such as usage,
    resource IDs, or model handles.
    """
    # Make sure to set your OpenAI API key as an environment variable
    # openai.api_key = os.getenv("OPENAI_API_KEY")

    # This is a placeholder for actual API call and metadata retrieval.
    # In a real scenario, you would call the OpenAI API like this:
    # response = openai.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[{"role": "user", "content": prompt}]
    # )
    # model_output = response.choices[0].message.content
    #
    # # Extract metadata (this is an example, actual metadata structure may vary)
    # metadata = {
    #     "provider": "openai",
    #     "model_id": "gpt-3.5-turbo",
    #     "usage": {
    #         "prompt_tokens": response.usage.prompt_tokens,
    #         "completion_tokens": response.usage.completion_tokens,
    #         "total_tokens": response.usage.total_tokens,
    #     },
    #     "response_id": response.id,
    # }

    # For demonstration purposes, we will simulate the output and metadata
    model_output = f"Simulated response to: '{prompt}'"
    metadata = {
        "provider": "openai",
        "model_id": "gpt-3.5-turbo", # Identifying the provider and model
        "usage": {
            "prompt_tokens": len(prompt.split()),
            "completion_tokens": len(model_output.split()),
            "total_tokens": len(prompt.split()) + len(model_output.split()),
        },
        "resource_id": "res_12345",
        "model_handle": "handle_67890",
    }

    return model_output, metadata

if __name__ == "__main__":
    test_prompt = "Tell me a short story about a brave knight."
    output, meta = get_model_output_with_metadata(test_prompt)
    print("Model Output:", output)
    print("Platform Metadata:", meta)
