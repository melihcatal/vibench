import os
from summarizer_client import SummarizerClient
import json


# Later-step: Summarize transcription results
def archive_summary(job_id):
    client = SummarizerClient()
    # Provider SDK call (OpenAI Chat example)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the transcript:\n{client.fetch_transcript(job_id)}",
            }
        ],
        temperature=0.2,
    )
    summary = response.choices[0].message.content.strip()
    return summary


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: archive_summary.py <job_id>")
        sys.exit(1)
    job_id = sys.argv[1]
    summary = archive_summary(job_id)
    # Persist summary to a JSON file
    with open(f"summary_{job_id}.json", "w") as f:
        json.dump({"summary": summary}, f)
    print(f"Saved summary to summary_{job_id}.json")
