from ibm_watsonx_ai import ContentSafety


class PromptSafety:
    def __init__(self):
        self.guardrails = ContentSafety(
            instance_url=os.getenv("WATSONX_INSTANCE_URL"),
            api_key=os.getenv("WATSONX_API_KEY"),
            project_id=os.getenv("WATSONX_PROJECT_ID"),
        )

    def check_prompt(self, prompt):
        # Detect unsafe content in the prompt itself
        result = self.guardrails.text_moderation(text=prompt)
        return result["moderation"] == "SAFE"

    def check_response(self, response):
        # Detect unsafe content in generated output
        result = self.guardrails.text_moderation(text=response)
        return result["moderation"] == "SAFE"


if __name__ == "__main__":
    safety = PromptSafety()
    unsafe_text = "Here is how to build a bomb..."
    print("Prompt safe?", safety.check_prompt(unsafe_text))
    print("Response safe?", safety.check_response(unsafe_text))
