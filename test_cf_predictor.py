"""
Tests for CashFlowPredictor using the real accounting-export layout:
company header row (col A only) -> invoice rows (due date col N=13,
Rozdiel col AD=29) -> subtotal row. Run: python test_cf_predictor.py
"""

import sys
import pandas as pd
from datetime import datetime, timedelta
from cf_predictor import CashFlowPredictor

today = datetime(2026, 10, 22)
failures = []


def check(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        failures.append(name)


def make_export(companies):
    """companies: list of (name, [(due_date, rozdiel), ...]) -> raw DataFrame like pd.read_excel(header=None)."""
    rows = []

    def blank():
        return [None] * 32

    r = blank(); r[0] = "Nevyrovnané pohľadávky k 22. 10. 2026"; rows.append(r)
    r = blank(); r[0] = "Názov firmy"; r[13] = "Dátum splatnosti"; r[29] = "Rozdiel"; rows.append(r)
    for name, items in companies:
        r = blank(); r[0] = name; rows.append(r)
        for due, roz in items:
            r = blank(); r[13] = due; r[23] = abs(roz) + 100; r[29] = roz; rows.append(r)
        r = blank(); r[29] = sum(x[1] for x in items); rows.append(r)  # subtotal, no due date
    r = blank(); r[0] = "CELKOM"; rows.append(r)
    return pd.DataFrame(rows)


p = CashFlowPredictor(today=today)

# --- Receivables: overdue 70+ days dropped, 0-69 overdue kept, future kept
recv = make_export([
    ("Firma A", [(today - timedelta(days=69), 100.0),    # keep (overdue 69)
                 (today - timedelta(days=70), 200.0),    # drop (overdue 70)
                 (today - timedelta(days=200), 300.0)]), # drop
    ("Firma B", [(today + timedelta(days=30), 400.0),    # keep (future)
                 (today + timedelta(days=5), 0.0)]),     # drop (settled)
])
R = p.extract_receivables(recv)
check("receivables: 70+ days overdue excluded, others kept", sorted(R.amount) == [100.0, 400.0])
check("receivables: company name carried down from header row", set(R.company_name) == {"Firma A", "Firma B"})

# --- Payables: no age filter, negative items (credits) are netted
pay = make_export([
    ("Dodavatel X", [(today - timedelta(days=500), 1000.0),   # very old, still owed
                     (today + timedelta(days=3), -10.0),      # credit/overpayment
                     (today + timedelta(days=9), 0.0)]),      # settled
])
P = p.extract_payables(pay)
check("payables: old items kept, zero dropped", len(P) == 2)
check("payables: negative item kept", (P.amount < 0).sum() == 1)

# --- Forecast: variable horizon + opening balance
for n in (1, 4, 13, 26):
    f = p.generate_forecast(P, R, num_weeks=n, start_date=today, opening_balance=500.0)
    ok = (len([k for k in f['forecast'] if k.startswith('week_')]) == n
          and f['summary']['num_weeks'] == n)
    check(f"forecast: {n} weeks", ok)

f = p.generate_forecast(P, R, num_weeks=13, start_date=today, opening_balance=500.0)
w1 = f['forecast']['week_1']
# week 1: overdue payable 1000 + credit -10 = 990 out; receivables 100 (overdue 69d) in
check("week 1 payables = 990 (overdue + credit)", abs(w1['payables'] - 990.0) < 0.01)
check("week 1 receivables = 100", abs(w1['receivables'] - 100.0) < 0.01)
check("closing balance = opening + net", abs(w1['closing'] - (500.0 + w1['net'])) < 0.01)
check("HTML report renders for 13 weeks", len(p.generate_html_report(f)) > 1000)
f1 = p.generate_forecast(P, R, num_weeks=1, start_date=today)
check("HTML report renders for 1 week", len(p.generate_html_report(f1)) > 1000)

print()
if failures:
    print(f"{len(failures)} test(s) FAILED")
    sys.exit(1)
print("All tests passed")
