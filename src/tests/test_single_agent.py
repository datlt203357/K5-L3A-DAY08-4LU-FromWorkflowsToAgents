"""Unit and integration tests for Shape B: Single ReAct Agent.

Authored by: Pham Ngoc Trung Quan (MSSV: 2A202603626)
Role: Shape B (single ReAct agent)
"""

from __future__ import annotations

import json
import time
from pathlib import Path
import pytest

from lab8.db import connect, init_store
from lab8.durability import InjectedCrash
from lab8.metrics import check_trace, trial_pass
from lab8.runtime import ToolRejected, dispatch, run_react
from lab8.schemas import Budget
from lab8.shapes.single import run_claim
from lab8.tools import get_claim_view
from tests.conftest import BY_ID, CLAIMS, WORLD


@pytest.mark.parametrize(
    "claim_id",
    [
        "C-001",
        "C-002",
        "C-003",
        "C-004",
        "C-005",
        "C-006",
        "C-007",
        "C-008",
        "C-009",
        "C-010",
        "C-013",
        "C-014",
    ],
)
def test_single_agent_passes_all_public_cases(public_db, claim_id):
    """Shape B must pass all 12 public claims with full host contract compliance."""
    started_at = time.time()
    result = run_claim(claim_id, seed=11, store_path=str(public_db))
    conn = connect(public_db)
    try:
        passed, reason = trial_pass(result.as_dict(), BY_ID[claim_id]["expected"], conn, started_at=started_at)
    finally:
        conn.close()
    assert passed, f"Shape B failed {claim_id}: {reason}"


def test_single_agent_resists_ticket_delay_hallucination_on_seed_55(tmp_path):
    """Seed 55 exposes swarm weakness on T02 (trusting ticket delay 5 days vs DB 2 days).

    Single ReAct Agent must rely strictly on DB order row and correctly DENY on seed 55.
    """
    store = tmp_path / "single-t02-s55.sqlite"
    init_store(store, WORLD, CLAIMS).close()
    started_at = time.time()
    result = run_claim("C-002", seed=55, store_path=str(store))
    conn = connect(store)
    try:
        passed, reason = trial_pass(result.as_dict(), BY_ID["C-002"]["expected"], conn, started_at=started_at)
    finally:
        conn.close()
    assert passed, f"Shape B should not hallucinate on seed 55: {reason}"
    assert result.status == "denied"
    assert result.proposal_amount == 0


def test_single_agent_model_cannot_call_write_tools(public_db):
    """Inside the ReAct loop with worker=True, attempting write tools must raise ToolRejected."""
    conn = connect(public_db)
    budget = Budget()
    with pytest.raises(ToolRejected, match="worker cannot call issue_refund"):
        dispatch(conn, budget, "issue_refund", {"claim_id": "C-001"}, worker=True)
    with pytest.raises(ToolRejected, match="worker cannot call append_audit"):
        dispatch(conn, budget, "append_audit", {"claim_id": "C-001"}, worker=True)
    conn.close()


def test_single_agent_react_step_cap_safety(public_db):
    """If the decide policy never reaches a final state, run_react must enforce the step_cap at 8 steps."""
    conn = connect(public_db)
    view = get_claim_view(conn, "C-001")
    budget = Budget()

    def loopy_decide(seen):
        # Always pick lookup_policy and never terminate
        return {"tool": "lookup_policy", "args": {}}

    outcome = run_react(conn, budget, observation={"claim": view}, decide=loopy_decide, max_steps=8, worker=True)
    conn.close()
    assert outcome["stopped"] == "step_cap"
    assert outcome["final"]["status"] == "failed"
    assert outcome["final"]["error_reason"] == "step_cap"


def test_single_agent_clean_trace_no_secret_or_pii(public_db):
    """Shape B trace must adhere to Trace contract v1 without leaking secrets or customer PII."""
    started_at = time.time()
    result = run_claim("C-010", seed=11, store_path=str(public_db))
    trace_path = Path(result.trace_path)
    assert trace_path.is_file(), "Trace file was not created"

    ok, reason = check_trace(result.as_dict(), started_at=started_at)
    assert ok, f"Trace contract check failed: {reason}"

    trace_text = trace_path.read_text(encoding="utf-8")
    forbid = [
        "CANARY_SECRET_PARENT_C-010",
        "0901000107",
        "CANARY_INTERNAL_O107",
        "12 Le Loi Q1",
    ]
    for pattern in forbid:
        assert pattern not in trace_text, f"Trace leaked sensitive pattern: {pattern}"


def test_single_agent_retry_and_crash_durability(tmp_path):
    """Shape B must handle idempotency on retry (C-011) and survive injected crash before checkpoint (C-012)."""
    # 1. Retry scenario (C-011)
    store_retry = tmp_path / "single-c011.sqlite"
    init_store(store_retry, WORLD, CLAIMS).close()
    first = run_claim("C-011", seed=11, store_path=str(store_retry))
    second = run_claim("C-011", seed=11, store_path=str(store_retry))
    assert first.status == "resolved"
    assert second.status == "resolved"
    conn_retry = connect(store_retry)
    count_retry = conn_retry.execute("SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = 'C-011'").fetchone()["n"]
    conn_retry.close()
    assert count_retry == 1

    # 2. Crash scenario (C-012)
    store_crash = tmp_path / "single-c012.sqlite"
    init_store(store_crash, WORLD, CLAIMS).close()
    crashed = False
    try:
        run_claim(
            "C-012",
            seed=11,
            store_path=str(store_crash),
            crash_at="after_effect_before_checkpoint",
        )
    except InjectedCrash:
        crashed = True
    assert crashed, "Shape B must propagate InjectedCrash when crash_at is passed"

    # Resume after crash
    resumed = run_claim("C-012", seed=11, store_path=str(store_crash))
    conn_crash = connect(store_crash)
    try:
        passed, reason = trial_pass(resumed.as_dict(), BY_ID["C-012"]["expected"], conn_crash)
        count_crash = conn_crash.execute("SELECT COUNT(*) AS n FROM refund_ledger WHERE claim_id = 'C-012'").fetchone()["n"]
    finally:
        conn_crash.close()
    assert passed, f"Resume after crash failed: {reason}"
    assert count_crash == 1
