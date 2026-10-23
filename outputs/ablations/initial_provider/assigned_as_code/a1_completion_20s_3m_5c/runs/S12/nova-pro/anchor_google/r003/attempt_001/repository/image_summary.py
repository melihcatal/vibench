def summarize_visual_analysis(analysis_results):
    summary = {
        'labels': [label['name'] for label in analysis_results['labels']],
        'description': analysis_results['description'],
        'text': analysis_results['text'],
        'safety': analysis_results['safety'],
    }
    return summary