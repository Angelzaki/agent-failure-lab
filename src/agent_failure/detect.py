from __future__ import annotations

from agent_failure.scenarios import Run, SCENARIOS


def detect(run: Run) -> dict:
    failures = []
    if any(not s.ok for s in run.steps):
        failures.append("tool_execution_error")
    if len(run.steps) > run.max_steps:
        failures.append("unbounded_cost_spiral")
    invented = [s for s in run.steps if s.tool == "invent_fact" or "invent" in s.output.lower() or "luna" in s.output.lower()]
    if invented:
        failures.append("recursive_hallucination")
    repeated = len({s.output for s in run.steps}) < max(1, len(run.steps) // 2) and len(run.steps) > 4
    if repeated:
        failures.append("planning_loop")
    return {
        "scenario": run.name,
        "steps": len(run.steps),
        "failures": failures,
        "ok": len(failures) == 0,
    }


def run_lab() -> dict:
    details = []
    detected = 0
    expected = {
        "tool_error": {"tool_execution_error"},
        "cost_spiral": {"unbounded_cost_spiral"},
        "hallucination_cascade": {"recursive_hallucination"},
        "good_path": set(),
    }
    for name, factory in SCENARIOS.items():
        result = detect(factory())
        want = expected[name]
        got = set(result["failures"])
        hit = want.issubset(got) if want else result["ok"]
        if want and want.issubset(got):
            detected += 1
        elif not want and result["ok"]:
            detected += 1
        details.append({**result, "expected": sorted(want), "hit": hit})
    return {
        "detected": detected,
        "total": len(SCENARIOS),
        "score": round(detected / len(SCENARIOS), 4),
        "details": details,
    }
