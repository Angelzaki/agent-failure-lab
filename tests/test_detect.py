from agent_failure.detect import detect, run_lab
from agent_failure.scenarios import scenario_cost_spiral, scenario_good


def test_detect_spiral():
    result = detect(scenario_cost_spiral())
    assert "unbounded_cost_spiral" in result["failures"]


def test_good_ok():
    assert detect(scenario_good())["ok"] is True


def test_lab_score():
    assert run_lab()["score"] >= 0.75
