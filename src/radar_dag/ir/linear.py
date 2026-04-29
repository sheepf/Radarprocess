from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping, Sequence


@dataclass(frozen=True)
class LinearStep:
    name: str
    op: str
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    parameters: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "op": self.op,
            "inputs": list(self.inputs),
            "outputs": list(self.outputs),
            "parameters": dict(self.parameters),
        }


@dataclass(frozen=True)
class LinearIR:
    name: str
    steps: tuple[LinearStep, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "metadata": dict(self.metadata),
            "steps": [step.to_dict() for step in self.steps],
        }


def load_linear_ir(path: str | Path) -> LinearIR:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, Mapping):
        raise ValueError("linear IR file must contain a JSON object")
    return linear_ir_from_dict(payload)


def linear_ir_from_dict(payload: Mapping[str, Any]) -> LinearIR:
    name = _require_non_empty_string(payload, "name")
    steps_raw = payload.get("steps")
    if not isinstance(steps_raw, Sequence) or isinstance(steps_raw, (str, bytes)):
        raise ValueError("steps must be a list of step objects")

    steps = tuple(_step_from_dict(item, index) for index, item in enumerate(steps_raw))
    if not steps:
        raise ValueError("linear IR must contain at least one step")

    metadata = _optional_mapping(payload.get("metadata"), "metadata")
    return LinearIR(name=name, steps=steps, metadata=metadata)


def linear_ir_to_dict(ir: LinearIR) -> dict[str, Any]:
    return ir.to_dict()


def _step_from_dict(item: Any, index: int) -> LinearStep:
    if not isinstance(item, Mapping):
        raise ValueError(f"step {index} must be a JSON object")

    return LinearStep(
        name=_require_non_empty_string(item, "name", prefix=f"step {index}"),
        op=_require_non_empty_string(item, "op", prefix=f"step {index}"),
        inputs=_string_sequence(item.get("inputs"), field_name=f"step {index}.inputs"),
        outputs=_string_sequence(item.get("outputs"), field_name=f"step {index}.outputs"),
        parameters=_optional_mapping(item.get("parameters"), f"step {index}.parameters"),
    )


def _require_non_empty_string(payload: Mapping[str, Any], key: str, prefix: str = "") -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        label = f"{prefix}.{key}" if prefix else key
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()


def _string_sequence(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{field_name} must be a list of strings")

    items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name}[{index}] must be a non-empty string")
        items.append(item.strip())
    return tuple(items)


def _optional_mapping(value: Any, field_name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, Mapping):
        raise ValueError(f"{field_name} must be an object")
    return dict(value)
