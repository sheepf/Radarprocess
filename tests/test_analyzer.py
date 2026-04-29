from pathlib import Path

from radar_dag.ir.linear import load_linear_ir, linear_ir_from_dict
from radar_dag.pipeline.analyzer import analyze_linear_ir, render_text_report


def sample_payload() -> dict[str, object]:
    return {
        "name": "demo_ir",
        "metadata": {"domain": "radar"},
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


def test_linear_ir_from_dict_parses_steps() -> None:
    ir = linear_ir_from_dict(sample_payload())

    assert ir.name == "demo_ir"
    assert ir.metadata == {"domain": "radar"}
    assert ir.steps[0].name == "load_echo"
    assert ir.steps[1].inputs == ("echo",)
    assert ir.to_dict()["steps"][1]["outputs"] == ["compressed"]


def test_load_linear_ir_reads_json(tmp_path: Path) -> None:
    file_path = tmp_path / "sample_ir.json"
    file_path.write_text(
        """
        {
          "name": "demo_ir",
          "steps": [
            {"name": "load_echo", "op": "load", "outputs": ["echo"]}
          ]
        }
        """,
        encoding="utf-8",
    )

    ir = load_linear_ir(file_path)

    assert ir.name == "demo_ir"
    assert ir.steps[0].op == "load"


def test_analyze_linear_ir_returns_order_and_report_text() -> None:
    ir = linear_ir_from_dict(sample_payload())
    report = analyze_linear_ir(ir)

    assert report.step_count == 2
    assert report.execution_order == ("load_echo", "matched_filter")
    assert report.warnings == ()
    assert "Linear IR report: demo_ir" in render_text_report(report)
