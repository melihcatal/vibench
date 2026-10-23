"""Continue stopped ablation 1; new attempts have a five-minute budget."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[4]))
from ablations.initial_provider.assigned_as_code.scripts import run
from ablations.shared.common import HERE, ROOT
from ablations.shared.timeout_continuation import launch

if __name__ == '__main__':
    launch(run, HERE / 'initial_provider/assigned_as_code/config_completion.yaml', ROOT / 'outputs/ablations/initial_provider/assigned_as_code/a1_completion_20s_3m_5c')
