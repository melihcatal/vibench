import os
from google.cloud import perspective
from google.cloud.perspective import types

def moderate_text(text):
    client = perspective.PerspectiveClient()
    comment = types.Comment(text=text)
    request = types.AnalyzeCommentRequest(
        comment=comment,
        requested_attributes={'TOXICITY': {}}
    )
    response = client.analyze_comment(request=request)
    return response.attribute_scores['TOXICITY'].summary_score.value >= 0.5