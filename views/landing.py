import streamlit as st

st.markdown("""
<div style='text-align: center; padding: 40px 10px;'>
    <div style='display: inline-block; background: linear-gradient(135deg, #3B82F6, #8B5CF6); padding: 16px; border-radius: 20px; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.5);'>
        <h1 style='margin: 0; font-size: 48px; line-height: 1;'>🎓</h1>
    </div>
    <h1 style='font-size: 48px; margin-bottom: 16px; font-weight: 800; background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>EduSafe AI™</h1>
    <p style='font-size: 20px; color: var(--text-muted); max-width: 600px; margin: 0 auto; line-height: 1.6;'>
        Next-Generation Predictive Early Warning & Explainable Intervention Architecture.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="responsive-flex" style="display: flex; gap: 24px; margin-bottom: 40px;">
    <div class="premium-card" style="flex: 1; margin-bottom: 0;">
        <h3 style="color: #60A5FA !important; display: flex; align-items: center; gap: 8px; margin: 0;">💡 Intelligent Explanations</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin-top: 12px; margin-bottom: 0;">Powered by localized SHAP and LIME boundaries for deep insights.</p>
    </div>
    <div class="premium-card" style="flex: 1; margin-bottom: 0;">
        <h3 style="color: #34D399 !important; display: flex; align-items: center; gap: 8px; margin: 0;">⚖️ Cross-Model Alignment</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin-top: 12px; margin-bottom: 0;">Validates risk assertions dynamically across Tree-Ensembles and Boosting networks.</p>
    </div>
    <div class="premium-card" style="flex: 1; margin-bottom: 0;">
        <h3 style="color: #F87171 !important; display: flex; align-items: center; gap: 8px; margin: 0;">🎯 Prescriptive Runbooks</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin-top: 12px; margin-bottom: 0;">Immediate action blueprints tailored to student metric vulnerabilities.</p>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("🚀 Initialize Risk Analysis Intake", type="primary", use_container_width=True):
        st.switch_page("views/input_form.py")
