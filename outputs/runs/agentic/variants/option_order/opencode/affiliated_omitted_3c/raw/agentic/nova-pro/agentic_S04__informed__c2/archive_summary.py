from transformers import pipeline


def archive_summary(text):
    summarizer = pipeline("summarization")
    return summarizer(text, max_length=130, min_length=30, do_sample=False)[0][
        "summary_text"
    ]
