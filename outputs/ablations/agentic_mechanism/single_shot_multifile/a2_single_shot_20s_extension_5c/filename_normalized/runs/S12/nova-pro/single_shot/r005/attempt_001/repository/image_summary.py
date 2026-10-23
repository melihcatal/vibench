from vision_models import ImageAnalysisResponse

def image_summary(analysis_response: ImageAnalysisResponse):
    summary = {}
    summary['objects'] = [obj['name'] for obj in analysis_response.get_objects()]
    summary['caption'] = analysis_response.get_caption()[0]['text']
    summary['text'] = [text['text'] for text in analysis_response.get_text()]
    summary['adult'] = analysis_response.get_adult()
    return summary