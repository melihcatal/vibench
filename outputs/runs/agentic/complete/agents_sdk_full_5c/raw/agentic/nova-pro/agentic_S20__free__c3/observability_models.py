class LogQuery:
    def __init__(self, query):
        self.query = query

class LogResponse:
    def __init__(self, status, tables):
        self.status = status
        self.tables = tables