# NyayaRent AI MVP

A rule-based first prototype for Uttar Pradesh rental security-deposit disputes.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Current capability

- Captures structured case facts
- Checks preliminary applicability inputs
- Calculates the Section 11 deposit ceiling
- Separates factual inputs from legal explanation
- Produces an evidence checklist
- Drafts a first landlord message

## Important limitation

Before public deployment, replace the source note in `legal_kb.json` with the exact official government source URL and verify the complete statutory text. Do not add a legal rule unless it has been checked against an official source.
