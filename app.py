import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="NyayaRent AI", page_icon="⚖️", layout="centered")
KB = json.loads(Path("legal_kb.json").read_text(encoding="utf-8"))
SECTION_11 = KB["records"][0]

st.title("NyayaRent AI")
st.caption("Source-grounded help for rental security-deposit disputes in Uttar Pradesh")
st.warning("Prototype only. This is legal information, not a substitute for advice from a qualified lawyer.")

with st.form("case_form"):
    city = st.text_input("City", value="Varanasi")
    property_type = st.selectbox("Premises type", ["Residential", "Non-residential"])
    monthly_rent = st.number_input("Monthly rent (₹)", min_value=0, step=500, value=12000)
    deposit = st.number_input("Security deposit paid (₹)", min_value=0, step=500, value=30000)
    possession = st.selectbox("Have you returned vacant possession and keys?", ["Yes", "No", "Not sure"])
    deduction = st.number_input("Deduction claimed by landlord (₹)", min_value=0, step=500, value=10000)
    reason = st.text_input("Reason given for deduction", value="Painting")
    invoice = st.selectbox("Did the landlord provide a bill or itemised statement?", ["No", "Yes", "Not sure"])
    evidence = st.multiselect(
        "Evidence available",
        ["Tenancy agreement", "Deposit payment proof", "Move-out photographs", "Key handover proof", "Utility receipts", "Landlord messages"],
        default=["Tenancy agreement", "Deposit payment proof", "Move-out photographs"]
    )
    story = st.text_area("Optional: describe the dispute in your own words")
    submitted = st.form_submit_button("Analyse my case")

if submitted:
    multiplier = 2 if property_type == "Residential" else 6
    ceiling = monthly_rent * multiplier
    excess = max(0, deposit - ceiling)

    st.subheader("1. Facts supplied")
    st.json({
        "state": "Uttar Pradesh",
        "city": city,
        "premises_type": property_type,
        "monthly_rent": monthly_rent,
        "security_deposit": deposit,
        "vacant_possession_returned": possession,
        "claimed_deduction": deduction,
        "deduction_reason": reason,
        "itemised_support": invoice,
        "evidence": evidence,
        "user_story": story
    })

    st.subheader("2. Applicability checks")
    checks = []
    checks.append("✓ Property reported to be in Uttar Pradesh")
    checks.append("✓ Premises type recorded")
    checks.append("✓ Deposit and monthly-rent figures supplied")
    checks.append("✓ Vacant possession reported as returned" if possession == "Yes" else "⚠ Refund-stage analysis is incomplete because vacant possession is not confirmed")
    checks.append("⚠ Covered urban-area and statutory-exclusion checks still require confirmation")
    for item in checks:
        st.write(item)

    st.subheader("3. Section 11 calculation")
    st.metric("Calculated deposit ceiling", f"₹{ceiling:,.0f}")
    if excess:
        st.error(f"Reported deposit is ₹{excess:,.0f} above the calculated {multiplier}-month ceiling.")
    else:
        st.success("Reported deposit does not exceed the calculated ceiling.")

    st.subheader("4. Preliminary legal explanation")
    st.write(
        f"Section 11 of the Uttar Pradesh Regulation of Urban Premises Tenancy Act, 2021 states that the security deposit for "
        f"{property_type.lower()} premises must not exceed {multiplier} months' rent. Using the figures supplied, the calculated ceiling is "
        f"₹{ceiling:,.0f}. The provision also addresses refund after vacant possession, subject to deduction of the tenant's liabilities."
    )
    if deduction > 0:
        st.write(
            f"The claimed ₹{deduction:,.0f} deduction for {reason or 'the stated reason'} is not automatically treated as valid or invalid. "
            "The agreement, condition of the premises, responsibility for the expense, and supporting documents must be examined."
        )

    st.subheader("5. Evidence check")
    missing = []
    for required in ["Tenancy agreement", "Deposit payment proof", "Move-out photographs", "Key handover proof", "Utility receipts", "Landlord messages"]:
        if required not in evidence:
            missing.append(required)
    if invoice != "Yes":
        missing.append("Landlord's itemised deduction statement or invoice")
    st.write("**Available:** " + (", ".join(evidence) if evidence else "None selected"))
    st.write("**Still useful:** " + (", ".join(missing) if missing else "No major item identified"))

    st.subheader("6. Draft first message")
    message = (
        f"Hello, I have returned the rented premises and keys. Please provide an itemised written statement and supporting documents for "
        f"the proposed ₹{deduction:,.0f} deduction for {reason or 'the claimed liability'}. I also request repayment of the balance security "
        "deposit within seven days. Please confirm the repayment date in writing."
    )
    st.code(message, language=None)

    st.subheader("7. Verified source record used")
    st.write(f"**{SECTION_11['law']}, Section {SECTION_11['section']}**")
    for rule in SECTION_11["verified_rules"]:
        st.write("- " + rule)
    st.info(SECTION_11["official_source_note"])
