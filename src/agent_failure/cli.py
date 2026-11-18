from __future__ import annotations

import argparse
import json
from pathlib import Path

from rich.console import Console
from rich.table import Table

from agent_failure.detect import run_lab

console = Console()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="agent-failure")
    parser.add_argument("--results", default="results")
    args = parser.parse_args(argv)
    report = run_lab()
    out = Path(args.results)
    out.mkdir(parents=True, exist_ok=True)
    (out / "agent_failures.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    table = Table(title="Agent Failure Lab")
    table.add_column("scenario")
    table.add_column("failures")
    table.add_column("hit")
    for d in report["details"]:
        table.add_row(d["scenario"], ",".join(d["failures"]) or "—", "yes" if d["hit"] else "no")
    console.print(table)
    console.print(f"score={report['score']:.0%}")
    return 0 if report["score"] >= 0.75 else 1


if __name__ == "__main__":
    raise SystemExit(main())
