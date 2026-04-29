from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from radar_dag.ir.linear import LinearIR


@dataclass(frozen=True)
class StepSummary:
    index: int
    name: str
    op: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "name": self.name,
            "op": self.op,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
        }


@dataclass(frozen=True)
class LinearAnalysisReport:
    name: str
    step_count: int
    execution_order: tuple[str, ...]
    summaries: tuple[StepSummary, ...]
    warnings: tuple[str, ...]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "step_count": self.step_count,
            "execution_order": list(self.execution_order),
            "summaries": [summary.to_dict() for summary in self.summaries],
            "warnings": list(self.warnings),
            "metadata": dict(self.metadata),
        }


def analyze_linear_ir(ir: LinearIR) -> LinearAnalysisReport:
    summaries: list[StepSummary] = []
    warnings: list[str] = []
    known_values: set[str] = set()

    for index, step in enumerate(ir.steps):
        summaries.append(
            StepSummary(
                index=index,
                name=step.name,
                op=step.op,
                inputs=step.inputs,
                outputs=step.outputs,
            )
        )

        if index == 0 and step.inputs:
            warnings.append(f"step '{step.name}' declares inputs even though it is the first step")

        missing_inputs = [value for value in step.inputs if value not in known_values]
        if index > 0 and missing_inputs:
            warnings.append(
                f"step '{step.name}' uses inputs that were not produced earlier: {', '.join(missing_inputs)}"
            )

        if not step.outputs:
            warnings.append(f"step '{step.name}' does not declare any outputs")

        known_values.update(step.outputs)

    return LinearAnalysisReport(
        name=ir.name,
        step_count=len(ir.steps),
        execution_order=tuple(step.name for step in ir.steps),
        summaries=tuple(summaries),
        warnings=tuple(warnings),
        metadata=dict(ir.metadata),
    )


def render_text_report(report: LinearAnalysisReport) -> str:
    lines = [
        f"Linear IR report: {report.name}",
        f"Step count: {report.step_count}",
        "Execution order:",
    ]
    for index, step_name in enumerate(report.execution_order, start=1):
        lines.append(f"  {index}. {step_name}")

    lines.append("Operations:")
    for summary in report.summaries:
        lines.append(f"  {summary.index + 1}. {summary.name} [{summary.op}]")
        lines.append(f"     inputs: {', '.join(summary.inputs) if summary.inputs else '-'}")
        lines.append(f"     outputs: {', '.join(summary.outputs) if summary.outputs else '-'}")

    lines.append("Warnings:")
    if report.warnings:
        for warning in report.warnings:
            lines.append(f"  - {warning}")
    else:
        lines.append("  - none")

    return "\n".join(lines)
