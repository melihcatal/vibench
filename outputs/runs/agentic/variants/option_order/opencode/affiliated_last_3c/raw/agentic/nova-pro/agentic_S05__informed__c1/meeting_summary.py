from transformers import pipeline


def meeting_summary(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)[0][
        "summary_text"
    ]
    return summary
