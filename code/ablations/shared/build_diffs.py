"""Export prompt comparisons into diffs/ for both ablations without model calls."""
import argparse
import difflib
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from ablations.initial_provider.assigned_as_code.scripts import build_inputs as inputs
from ablations.agentic_mechanism.single_shot_multifile.scripts import run as multi_file
from ablations.shared.runtime import agentic as runtime


def desired_diffs():
    files = {name: content for name, content in inputs.desired_files().items()
             if name.startswith('diffs/initial_provider/assigned_as_code/')}
    for scenario in inputs.SCENARIOS:
        agentic = multi_file.cell_inputs('agentic', scenario, 'nova-pro')
        single = multi_file.cell_inputs('single_shot', scenario, 'nova-pro')
        pairs = {
            'user_prompt': (agentic['prompt'], single['prompt']),
            'system_prompt': (runtime._build_opencode_agent_prompt(agentic['system']), single['system']),
        }
        for kind, (before, after) in pairs.items():
            # Normalize only the display newline so the final changed lines stay readable.
            files[f'diffs/agentic_mechanism/single_shot_multifile/{scenario}_{kind}.diff'] = ''.join(difflib.unified_diff(
                (before.rstrip('\n') + '\n').splitlines(keepends=True),
                (after.rstrip('\n') + '\n').splitlines(keepends=True),
                fromfile=f'agentic/{scenario}/{kind}.txt',
                tofile=f'single_shot/{scenario}/{kind}.txt'))
    return files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh-generated', action='store_true')
    args = parser.parse_args()
    files = desired_diffs()
    obsolete = []
    for name, content in files.items():
        if name.startswith('diffs/initial_provider/assigned_as_code/'):
            old = inputs.HERE / 'diffs' / name.rsplit('/', 1)[1]
            if old.exists():
                if old.read_text() != content:
                    raise ValueError(f'Refusing to remove edited legacy diff: {old}')
                obsolete.append(old)
    inputs.materialize(files, refresh=args.refresh_generated)
    for old in obsolete:
        old.unlink()
    print(f'Checked/materialized {len(files)} diffs in initial_provider/assigned_as_code/ and single_shot_multifile/. No model calls.')


if __name__ == '__main__':
    main()
