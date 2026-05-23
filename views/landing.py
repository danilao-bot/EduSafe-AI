import streamlit as st

st.markdown("""
<div style='display: flex; align-items: center; gap: 16px; margin-top: 20px; margin-bottom: 10px;'>
    <div style='background-color: #3B82F6; padding: 12px; border-radius: 12px; color: white;'>
        <h2 style='margin: 0; font-size: 32px;'>[SCHOOL]</h2>
    </div>
    <div>
        <h1 style='margin: 0; font-size: 32px; color: #1E293B;'>EduSafe AI™</h1>
        <p style='margin: 0; color: #64748B; font-size: 16px;'>Predictive Early Warning & Explainable Intervention Architecture</p>
    </div>
</div>
<hr style='border: 0; border-top: 1px solid rgba(128, 128, 128, 0.2); margin: 20px 0;'/>
""", unsafe_allow_html=True)

col_hero, _ = st.columns([2, 1])

with col_hero:
    st.markdown("### [ROBOT] Agentic Student Risk Diagnostics")
    st.markdown("""
    Welcome to the **EduSafe AI™ Student Success Portal**. This dashboard decouples complex predictive logic from static tracking. 
    By processing behavioral data patterns, financial metrics, and academic milestones, the predictive models run deep feature point checks 
    to prevent student attrition before it manifests.
    
    * **Intelligent Local Explanations:** Powered by SHAP and LIME tabular boundaries.
    * **Cross-Model Alignment:** Validates risk assertions across Tree-Ensembles and Boosting networks.
    * **Prescriptive Runbooks:** Immediate action blueprints tailored to local metric vulnerabilities.
    """)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    if st.button("Initialize Risk Analysis Intake [->]", type="primary"):
        st.switch_page("views/input_form.py")
