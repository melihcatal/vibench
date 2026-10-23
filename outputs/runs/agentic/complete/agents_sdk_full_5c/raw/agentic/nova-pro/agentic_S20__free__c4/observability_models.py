class StructuredLogModel:
    def to_query(self):
        return 'CustomLog | extend timestamp = now(), log_level = "INFO", message = "This is a structured log"'

class CorrelatedLogModel:
    def to_query(self):
        return 'CustomLog | extend timestamp = now(), log_level = "INFO", message = "This is a correlated log", correlation_id = "12345"'