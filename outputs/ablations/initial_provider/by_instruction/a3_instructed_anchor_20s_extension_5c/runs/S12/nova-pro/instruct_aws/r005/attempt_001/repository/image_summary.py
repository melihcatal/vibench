def summarize_visual_analysis(labels, description, text_detections, moderation_labels):
    summary = {
        'labels': labels,
        'description': description,
        'text_detections': text_detections,
        'moderation_labels': moderation_labels
    }
    return summary