"""Tests for Orchestrator shape (Shape C). Author: Member 3.

Covers:
1. Handoff security: ensuring no secret or raw parent context leaks into trace.
2. Partial compensation: verifying full quote proposal and difference calculation on previously refunded orders (T14).
3. Access boundary: verifying escalation when accessing orders outside principal scope (T05).
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from lab8.db import connect
from lab8.durability import get_refund
from lab8.shapes.orchestrator import run_claim


def test_orchestrator_handoff_has_no_secrets(public_db):
    """Test that handoff package strips all parent secrets and only grants read tools."""
    result = run_claim("C-010", seed=11, store_path=str(public_db))
    assert result.status == "resolved"
    assert result.proposal_amount == 35000

    trace_path = Path(result.trace_path)
    assert trace_path.exists()
    trace_raw = trace_path.read_text(encoding="utf-8")
    assert "CANARY_SECRET_" not in trace_raw
    assert "parent_secret" not in trace_raw

    trace_data = json.loads(trace_raw)
    handoff_events = [e for e in trace_data.get("events", []) if e.get("kind") == "handoff"]
    assert len(handoff_events) == 1
    handoff_payload = handoff_events[0]["payload"]
    assert "contract_version" in handoff_payload
    assert set(handoff_payload.get("allowed_tools", [])) <= {
        "lookup_order",
        "lookup_policy",
        "compute_compensation",
    }


def test_orchestrator_partial_difference_on_prior_refund(public_db):
    """Test T14: Order O-515 was previously refunded 30k ship fee.

    New damage entitlement is 150k. Orchestrator must quote full 150k, and host commits the 120k difference.
    """
    result = run_claim("C-014", seed=11, store_path=str(public_db))
    assert result.status == "resolved"
    assert result.proposal_amount == 150000
    conn = connect(public_db)
    try:
        refund = get_refund(conn, "C-014")
        assert refund is not None
        assert int(refund["amount_vnd"]) == 120000
    finally:
        conn.close()


def test_orchestrator_outside_principal_scope_escalates(public_db):
    """Test T05: Claim C-005 accesses an order owned by P-100 while principal is P-200.

    Must return escalated with 0 proposal and clean trace.
    """
    result = run_claim("C-005", seed=11, store_path=str(public_db))
    assert result.status == "escalated"
    assert result.proposal_amount == 0
    conn = connect(public_db)
    try:
        assert get_refund(conn, "C-005") is None
    finally:
        conn.close()
