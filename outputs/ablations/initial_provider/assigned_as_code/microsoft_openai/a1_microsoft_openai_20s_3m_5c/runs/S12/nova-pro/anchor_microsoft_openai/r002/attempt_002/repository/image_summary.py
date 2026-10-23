from summarizer import Summarizer

def summarize_image_analysis(analysis_results):
    model = Summarizer()
    summary = model(analysis_results)
    return summary