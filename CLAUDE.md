# CLAUDE.md

## Project rules

- Use Python 3.11+.
- Keep the first version focused on the CLI workflow: read a linear IR JSON file and print an analysis report.
- Prefer small, focused modules: IR parsing in `radar_dag/ir/`, analysis in `radar_dag/pipeline/`, CLI in `radar_dag/cli.py`.
- Do not add CUDA generation or multi-agent orchestration yet.
- Keep sample data in `examples/` and tests in `tests/`.
- Do not add a README unless explicitly requested.
