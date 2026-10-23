from google.ai.generativelanguage.v1beta2 import GenerateTextRequest, TextPrompt

def create_generate_text_request(model, prompt, temperature, candidate_count):
    return GenerateTextRequest(
        model=model,
        prompt=TextPrompt(text=prompt),
        temperature=temperature,
        candidate_count=candidate_count
    )