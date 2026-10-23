import os
import google.generativeai as genai


def moderation_summary(moderation_results):
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel("gemini-pro")

    prompt = f"Summarize the following moderation results. For each message, indicate if it was flagged and why (e.g., high toxicity, profanity). Also provide an overall summary of the moderation decisions:\n\n{moderation_results}"

    response = model.generate_content(prompt)
    return response.text


if __name__ == "__main__":
    # Example usage (requires GOOGLE_API_KEY environment variable to be set)
    # os.environ["GOOGLE_API_KEY"] = "YOUR_GOOGLE_API_KEY"
    if "GOOGLE_API_KEY" not in os.environ:
        print("Please set the GOOGLE_API_KEY environment variable.")
    else:
        sample_moderation_results = [
            {"text": "You are a fool!", "scores": {"TOXICITY": 0.9, "INSULT": 0.8}},
            {"text": "What a lovely day.", "scores": {"TOXICITY": 0.1}},
            {"text": "I hate this!", "scores": {"PROFANITY": 0.7}},
        ]
        summary = moderation_summary(sample_moderation_results)
        print("Moderation Summary:")
        print(summary)
