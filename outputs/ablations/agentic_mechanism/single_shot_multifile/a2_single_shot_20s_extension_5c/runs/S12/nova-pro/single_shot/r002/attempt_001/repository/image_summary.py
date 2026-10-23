from vision_models import VisionResponse

def summarize_analysis(analysis_response):
    vr = VisionResponse(analysis_response)
    labels = vr.get_labels()
    text = vr.get_text()
    safety = vr.get_safety()
    return f'Labels: {labels}, Text: {text}, Safety: {safety}'