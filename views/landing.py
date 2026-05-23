import streamlit as st

st.markdown("""
<div style='text-align: center; padding: 60px 10px; margin-bottom: 20px;'>
    <div style='display: inline-block; background: linear-gradient(135deg, #3B82F6, #8B5CF6); padding: 16px; border-radius: 20px; margin-bottom: 24px; box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.5);'>
        <h1 style='margin: 0; font-size: 48px; line-height: 1;'>🎓</h1>
    </div>
    <h1 style='font-size: 56px; margin-bottom: 16px; font-weight: 800; background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>Stop Student Attrition Before It Happens.</h1>
    <p style='font-size: 20px; color: var(--text-muted); max-width: 700px; margin: 0 auto; line-height: 1.6;'>
        EduSafe AI™ is the next-generation predictive early warning system. We empower academic advisors with explainable AI to identify at-risk students and deploy targeted interventions.
    </p>
</div>
""", unsafe_allow_html=True)

col_cta1, col_cta2, col_cta3, col_cta4 = st.columns([1, 1.5, 1.5, 1])
with col_cta2:
    if st.button("🚀 Run Live Diagnostics", type="primary", use_container_width=True):
        st.switch_page("views/input_form.py")
with col_cta3:
    if st.button("📖 View Model Architecture", type="secondary", use_container_width=True):
        st.info("Technical documentation coming soon.")

st.markdown("""
<div style='text-align: center; margin: 60px 0 40px 0;'>
    <h2 style='font-size: 32px; font-weight: 700;'>How It Works</h2>
</div>
<div class="responsive-flex" style="display: flex; gap: 24px; margin-bottom: 40px; text-align: center;">
    <div class="premium-card" style="flex: 1; margin-bottom: 0;">
        <div style="width:64px; height:64px; margin: 0 auto 16px; background: linear-gradient(135deg, #1E3A5F, #3B82F6); border-radius: 18px; display:flex; align-items:center; justify-content:center; box-shadow: 0 8px 20px rgba(59,130,246,0.35);">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <ellipse cx="12" cy="5" rx="9" ry="3" stroke="#93C5FD" stroke-width="1.5"/>
                <path d="M3 5v5c0 1.657 4.029 3 9 3s9-1.343 9-3V5" stroke="#93C5FD" stroke-width="1.5"/>
                <path d="M3 10v5c0 1.657 4.029 3 9 3s9-1.343 9-3v-5" stroke="#93C5FD" stroke-width="1.5"/>
            </svg>
        </div>
        <h3 style="color: var(--text-main); margin-top: 0; margin-bottom: 8px;">Data Intake</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin: 0;">We ingest LMS engagement metrics, demographic proxies, and historical GPA data.</p>
    </div>
    <div class="premium-card" style="flex: 1; margin-bottom: 0;">
        <div style="width:64px; height:64px; margin: 0 auto 16px; background: linear-gradient(135deg, #2E1065, #8B5CF6); border-radius: 18px; display:flex; align-items:center; justify-content:center; box-shadow: 0 8px 20px rgba(139,92,246,0.35);">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="4" y="4" width="16" height="16" rx="2" stroke="#C4B5FD" stroke-width="1.5"/>
                <path d="M9 9h6M9 12h6M9 15h4" stroke="#C4B5FD" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="7" cy="9" r="1" fill="#C4B5FD"/>
                <circle cx="7" cy="12" r="1" fill="#C4B5FD"/>
                <circle cx="7" cy="15" r="1" fill="#C4B5FD"/>
            </svg>
        </div>
        <h3 style="color: var(--text-main); margin-top: 0; margin-bottom: 8px;">AI Inference</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin: 0;">Ensemble models (Random Forest & XGBoost) analyze behavioural datapoints in milliseconds.</p>
    </div>
    <div class="premium-card" style="flex: 1; margin-bottom: 0;">
        <div style="width:64px; height:64px; margin: 0 auto 16px; background: linear-gradient(135deg, #052E16, #10B981); border-radius: 18px; display:flex; align-items:center; justify-content:center; box-shadow: 0 8px 20px rgba(16,185,129,0.35);">
            <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="9" stroke="#6EE7B7" stroke-width="1.5"/>
                <circle cx="12" cy="12" r="4" stroke="#6EE7B7" stroke-width="1.5"/>
                <circle cx="12" cy="12" r="1" fill="#6EE7B7"/>
                <path d="M12 2v3M12 19v3M2 12h3M19 12h3" stroke="#6EE7B7" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
        </div>
        <h3 style="color: var(--text-main); margin-top: 0; margin-bottom: 8px;">Prescriptive Action</h3>
        <p style="color: var(--text-muted); font-size: 14px; margin: 0;">SHAP & LIME explain <em>why</em> a student is at risk, and our engine recommends the optimal intervention plan.</p>
    </div>
</div>

<div style='text-align: center; margin: 60px 0 40px 0;'>
    <h2 style='font-size: 32px; font-weight: 700;'>Platform Impact</h2>
</div>
<div class="responsive-flex" style="display: flex; gap: 24px; margin-bottom: 60px; text-align: center;">
    <div style="flex: 1;">
        <h1 style="font-size: 48px; color: #60A5FA; margin: 0;">94%</h1>
        <p style="color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Prediction Accuracy</p>
    </div>
    <div style="flex: 1;">
        <h1 style="font-size: 48px; color: #A78BFA; margin: 0;">50ms</h1>
        <p style="color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Live Inference Time</p>
    </div>
    <div style="flex: 1;">
        <h1 style="font-size: 48px; color: #34D399; margin: 0;">10+</h1>
        <p style="color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Explainable Features</p>
    </div>
</div>

<hr style='border: 0; border-top: 1px solid var(--border-color); margin: 40px 0 20px 0;'/>
<div style='text-align: center; color: var(--text-muted); font-size: 12px; margin-bottom: 20px;'>
    <p>&copy; 2026 EduSafe AI. All rights reserved.</p>
    <p>
        <a href="#" style="color: var(--accent); text-decoration: none; margin: 0 10px;">Privacy Policy</a> | 
        <a href="#" style="color: var(--accent); text-decoration: none; margin: 0 10px;">Terms of Service</a> | 
        <a href="#" style="color: var(--accent); text-decoration: none; margin: 0 10px;">Documentation</a>
    </p>
</div>
""", unsafe_allow_html=True)
