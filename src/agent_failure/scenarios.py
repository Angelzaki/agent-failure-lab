from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Step:
    tool: str
    ok: bool
    output: str


@dataclass
class Run:
    name: str
    steps: list[Step] = field(default_factory=list)
    max_steps: int = 6


def scenario_tool_error() -> Run:
    return Run(
        name="tool_error",
        steps=[
            Step("search_docs", True, "hit politica_a1"),
            Step("read_doc", False, "timeout"),
            Step("read_doc", False, "timeout"),
        ],
    )


def scenario_cost_spiral() -> Run:
    steps = [Step("search_docs", True, f"loop-{i}") for i in range(12)]
    return Run(name="cost_spiral", steps=steps, max_steps=6)


def scenario_hallucination_cascade() -> Run:
    return Run(
        name="hallucination_cascade",
        steps=[
            Step("search_docs", True, "no evidence"),
            Step("invent_fact", True, "A1 incluye viaje a la luna"),
            Step("search_docs", True, "query based on invented fact"),
        ],
    )


def scenario_good() -> Run:
    return Run(
        name="good_path",
        steps=[
            Step("search_docs", True, "hit limite_comercial"),
            Step("read_doc", True, "Límite S/ 250,000"),
            Step("answer", True, "El límite comercial es S/ 250,000"),
        ],
    )


SCENARIOS = {
    "tool_error": scenario_tool_error,
    "cost_spiral": scenario_cost_spiral,
    "hallucination_cascade": scenario_hallucination_cascade,
    "good_path": scenario_good,
}
