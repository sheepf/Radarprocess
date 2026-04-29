from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from radar_dag.ir.linear import load_linear_ir
from radar_dag.pipeline.analyzer import analyze_linear_ir, render_text_report
from radar_dag.utils.logging import configure_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="radar_dag", description="Analyze a linear radar IR JSON file")
    parser.add_argument("ir_file", type=Path, help="Path to the IR JSON file")
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Output format for the analysis report",
    )
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(args.verbose)

    try:
        linear_ir = load_linear_ir(args.ir_file)
        report = analyze_linear_ir(linear_ir)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(report.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(render_text_report(report))

    return 0
