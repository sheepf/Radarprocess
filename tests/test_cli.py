import json
import subprocess
import sys
from pathlib import Path


def test_module_cli_outputs_json(tmp_path: Path) -> None:
    file_path = tmp_path / "sample_ir.json"
    file_path.write_text(
        json.dumps(
            {
                "name": "demo_ir",
                "steps": [
                    {"name": "load_echo", "op": "load", "outputs": ["echo"]},
                    {
                        "name": "matched_filter",
                        "op": "convolve",
                        "inputs": ["echo"],
                        "outputs": ["compressed"],
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [sys.executable, "-m", "radar_dag", str(file_path), "--format", "json"],
        cwd=Path(__file__).resolve().parents[1],
        capture_output=True,
        text=True,
        check=False,
    )

    assert completed.returncode == 0
    payload = json.loads(completed.stdout)
    assert payload["name"] == "demo_ir"
    assert payload["step_count"] == 2
    assert payload["execution_order"] == ["load_echo", "matched_filter"]
