import vertexai


def initialize_vertex_ai(project_id: str, location: str):
    vertexai.init(project=project_id, location=location)
