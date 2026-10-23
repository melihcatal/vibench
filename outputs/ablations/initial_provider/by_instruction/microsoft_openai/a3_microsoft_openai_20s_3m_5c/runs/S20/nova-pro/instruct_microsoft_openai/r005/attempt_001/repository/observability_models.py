class LogEvent:
    def __init__(self, name, value):
        self.name = name
        self.value = value

class QueryResponse:
    def __init__(self, status, tables):
        self.status = status
        self.tables = tables