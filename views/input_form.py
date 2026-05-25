import streamlit as st
import pandas as pd
import sys
import os

# Add parent directory to path to import utils
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import convert_usd_to_naira

st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h2 style="font-size: 36px; margin-bottom: 8px; color: var(--text-main) !important;">Student Profile Setup</h2>
    <p style="color: var(--text-muted); font-size: 16px;">Load a pre-configured template or fill in the student's details manually below.</p>
</div>
""", unsafe_allow_html=True)

MOCK_PROFILES = {
    "Custom Profile (Fill Manually)": None,
    "Alex Rivera (High Risk of Attrition)": {
        'gpa': 1.6, 'attendance': 58, 'engagement': 0.32, 'income_proxy': 18000,
        'low_gpa_flag': 1, 'low_engagement_flag': 1, 'risk_score': 8,
        'Unemployment rate': 1, 'Age at enrollment': 23, 'Gender': 1
    },
    "Chloe Chen (Stellar Academic Standing)": {
        'gpa': 3.9, 'attendance': 98, 'engagement': 0.95, 'income_proxy': 65000,
        'low_gpa_flag': 0, 'low_engagement_flag': 0, 'risk_score': 1,
        'Unemployment rate': 0, 'Age at enrollment': 18, 'Gender': 0
    },
    "Jordan Smith (Borderline Warning)": {
        'gpa': 2.3, 'attendance': 76, 'engagement': 0.55, 'income_proxy': 32000,
        'low_gpa_flag': 0, 'low_engagement_flag': 0, 'risk_score': 5,
        'Unemployment rate': 1, 'Age at enrollment': 21, 'Gender': 1
    }
}

selected_preset = st.selectbox(
    "👤 Load a Pre-configured Student Profile for Quick Demo:",
    options=list(MOCK_PROFILES.keys())
)

preset_values = MOCK_PROFILES[selected_preset]
def get_val(key, default=None):
    if preset_values is not None and key in preset_values:
        return preset_values[key]
    return default

# ── Main Input Grid ──────────────────────────────────────────────────────────
st.markdown("""
<style>
    @media (max-width: 640px) {
        .input-grid { display: grid; grid-template-columns: 1fr; gap: 20px; }
    }
    @media (min-width: 641px) and (max-width: 1024px) {
        .input-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    }
    @media (min-width: 1025px) {
        .input-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("### Academic Records")

    gpa_val = get_val('gpa')
    gpa = st.number_input(
        'Current GPA',
        min_value=0.0, max_value=4.0,
        value=float(gpa_val) if gpa_val is not None else None,
        step=0.01,
        help="The student's overall grade point average, rated out of 4.0"
    )

    att_val = get_val('attendance')
    attendance_pct = st.slider(
        'Attendance (%)',
        min_value=0, max_value=100,
        value=int(att_val) if att_val is not None else 0,
        step=1,
        format="%d%%",
        help="Percentage of classes attended. e.g. 90 = 90%, 45 = 45%"
    )
    # Display a human-readable hint under the slider
    if att_val is not None or attendance_pct > 0:
        st.caption(f"📌 {attendance_pct}% of classes attended")

with col2:
    st.markdown("### Engagement & Concern")

    engagement_val = get_val('engagement')
    default_eng_idx = None if engagement_val is None else (
        0 if engagement_val >= 0.8 else (
        1 if engagement_val >= 0.5 else (
        2 if engagement_val >= 0.25 else 3))
    )
    engagement_desc = st.selectbox(
        'Online Course Activity',
        options=[
            "Very Active — logs in daily, completes quizzes",
            "Moderately Active — logs in weekly",
            "Rarely Active — logs in infrequently",
            "Inactive — hardly ever logs in"
        ],
        index=default_eng_idx,
        help="How often does the student use the online learning portal?"
    )
    engagement = None if engagement_desc is None else (
        0.85 if "Very Active" in engagement_desc else (
        0.55 if "Moderately Active" in engagement_desc else (
        0.28 if "Rarely Active" in engagement_desc else 0.12))
    )

    risk_val = get_val('risk_score', 0)
    risk_score_display = st.slider(
        "Counselor's Concern Level",
        min_value=1, max_value=10,
        value=int(risk_val) if risk_val else 1,
        step=1,
        help="Rate your personal concern for this student: 1 = No concern at all, 10 = Extremely concerned"
    )
    # Clear label beneath the slider
    concern_label = (
        "🟢 Low Concern" if risk_score_display <= 3 else
        "🟡 Moderate Concern" if risk_score_display <= 6 else
        "🔴 High Concern"
    )
    st.caption(f"{concern_label} (Score: {risk_score_display}/10)")

with col3:
    st.markdown("### Background Details")

    inc_val = get_val('income_proxy')
    income_proxy = st.number_input(
        'Estimated Family Income (NGN)',
        min_value=0, max_value=500000000,
        value=int(inc_val) if inc_val is not None else None,
        help="Approximate annual household income in NGN dollars"
    )

    emp_val = get_val('Unemployment rate')
    employment_status = st.selectbox(
        'Employment Status (Local Region)',
        options=[0, 1],
        index=int(emp_val) if emp_val is not None else None,
        format_func=lambda x: "Yes - Employed" if x == 1 else "No - Unemployed",
        help="Is there employment availability in the student's region? (0=No, 1=Yes)"
    )

    age_val = get_val('Age at enrollment')
    age = st.number_input(
        'Age When They Enrolled',
        min_value=15, max_value=90,
        value=int(age_val) if age_val is not None else None
    )

    gender_val = get_val('Gender')
    gender = st.selectbox(
        'Student Gender',
        options=[0, 1],
        index=int(gender_val) if gender_val is not None else None,
        format_func=lambda x: "Male" if x == 1 else "Female"
    )

# ── Submit Button ─────────────────────────────────────────────────────────────
st.markdown("<br/>", unsafe_allow_html=True)
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])

with col_btn2:
    if st.button("Run Risk Analysis", type="primary", use_container_width=True):
        missing = []
        if gpa is None: missing.append("Current GPA")
        if engagement is None: missing.append("Online Course Activity")
        if income_proxy is None: missing.append("Estimated Family Income")
        if employment_status is None: missing.append("Employment Status")
        if age is None: missing.append("Age When They Enrolled")
        if gender is None: missing.append("Student Gender")

        if missing:
            st.error(f"Please fill in the following fields before running: **{', '.join(missing)}**")
        else:
            # Convert attendance from 0–100 integer → 0.0–1.0 ratio for the model
            attendance_ratio = attendance_pct / 100.0
            # Convert risk_score from 1–10 scale → 0.0–1.0 ratio for the model
            risk_score_ratio = (risk_score_display - 1) / 9.0
            # Convert income from USD to Naira
            income_naira = convert_usd_to_naira(income_proxy)

            st.session_state.selected_preset_name = selected_preset
            st.session_state.student_data = {
                'gpa': gpa,
                'attendance': attendance_ratio,
                'engagement': engagement,
                'income_proxy': income_naira,
                'low_gpa_flag': 1 if gpa < 2.0 else 0,
                'low_engagement_flag': 1 if engagement < 0.4 else 0,
                'risk_score': risk_score_ratio,
                'Unemployment rate': employment_status,
                'Age at enrollment': age,
                'Gender': gender
            }
            st.switch_page("views/dashboard.py")
