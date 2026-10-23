"""Continue stopped ablation 4; new attempts have a five-minute budget."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.agentic_mechanism.task_disclosure.scripts import run
from ablations.shared.common import HERE, ROOT
from ablations.shared.timeout_continuation import launch

if __name__ == '__main__':
    launch(run, HERE / 'agentic_mechanism/task_disclosure/config.yaml', ROOT / 'outputs/ablations/agentic_mechanism/task_disclosure/a4_disclosure_6s_3m_5c')
