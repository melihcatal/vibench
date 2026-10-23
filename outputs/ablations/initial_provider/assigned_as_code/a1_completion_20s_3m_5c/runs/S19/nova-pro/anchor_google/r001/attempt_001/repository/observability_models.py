from google.cloud.monitoring_v3 import Aggregation, AlignmentPeriod


class Aggregation:
    class Aligner:
        ALIGN_MEAN = 'ALIGN_MEAN'


class AlignmentPeriod:
    def __init__(self, seconds):
        self.seconds = seconds