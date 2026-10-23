import os
import google.generativeai as genai

class MeetingSummarizer:
    """Summarizes live meeting transcript chunks using the Google Gemini API."""
    def __init__(self, model_name: str = "gemini-pro", generation_config: dict = None):
        self.model_name = model_name
        self.api_key = os.environ.get("GOOGLE_API_KEY")

        if not self.api_key:
            raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
        self.generation_config = generation_config or {
            "temperature": 0.2,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 500,
        }
        print(f"Google Gemini API client initialized with model: {model_name}")

    def summarize_chunk(self, transcript_chunk: str) -> str:
        """Summarizes a given chunk of meeting transcript."""
        if not transcript_chunk.strip():
            return ""

        prompt = (
            f"Summarize the following meeting transcript chunk concisely in one or two sentences. "
            f"Focus on key decisions, action items, or main topics discussed:\n\n{transcript_chunk}"
        )

        try:
            response = self.model.generate_content(prompt, generation_config=self.generation_config)
            summary = response.text.strip()
            return summary
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"[Summary Error: {e}]"

    def __call__(self, transcript_chunk: str) -> str:
        return self.summarize_chunk(transcript_chunk)

if __name__ == "__main__":
    print("Demonstrating meeting summarization with Google Gemini API.")
    try:
        summarizer = MeetingSummarizer()

        test_chunks = [
            "Alright team, let's start with the Q3 budget review. Sarah, can you walk us through the actuals versus forecast? We need to decide on the marketing spend for the next quarter and approve the new hiring plan for engineering. John mentioned some concerns about server costs, so let's address that.",
            "Okay, so Sarah presented the budget. We are slightly over in marketing but under in operations. John's server cost concerns are noted. Action item: Sarah to provide a detailed breakdown of marketing spend. Decision: Approve engineering hiring, re-evaluate server costs next month.",
            "The next agenda item is the product roadmap for Project Alpha. We are behind schedule due to resource constraints. We need to decide whether to push the launch date or allocate more resources from Project Beta. Emily from design shared some new mockups, which look promising.",
            "", # Empty chunk
            "The discussion then moved to the client feedback for the new mobile app. Many users are requesting a dark mode feature and improved notification controls. We agreed to prioritize dark mode for the next sprint and add notification controls to the backlog. The customer support team will send out a survey to gather more specific feedback on notifications."
        ]

        for i, chunk in enumerate(test_chunks):
            print(f"\n--- Chunk {i+1} ---")
            print(f"Transcript: {chunk}")
            summary = summarizer.summarize_chunk(chunk)
            print(f"Summary: {summary}")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
