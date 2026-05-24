import streamlit as st

# ── Responsive Hero Section ───────────────────────────────────────────────────
st.markdown("""
<style>
    @media (max-width: 768px) {
        .hero-title {
            font-size: 32px !important;
        }
        .hero-subtitle {
            font-size: 16px !important;
        }
        .hero-icon {
            font-size: 40px !important;
        }
        .hero-padding {
            padding: 40px 16px !important;
        }
    }
    
    @media (min-width: 769px) and (max-width: 1024px) {
        .hero-title {
            font-size: 44px !important;
        }
        .hero-subtitle {
            font-size: 18px !important;
        }
        .hero-padding {
            padding: 50px 20px !important;
        }
    }
    
    @media (min-width: 1025px) {
        .hero-title {
            font-size: 56px !important;
        }
        .hero-subtitle {
            font-size: 20px !important;
        }
        .hero-padding {
            padding: 60px 10px !important;
        }
    }
    
    .hero-icon {
        display: inline-block;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        padding: 12px;
        border-radius: 20px;
        margin-bottom: 20px;
        box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.5);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .hero-icon:hover {
        transform: scale(1.1) translateY(-5px);
        box-shadow: 0 15px 35px -5px rgba(59, 130, 246, 0.6);
    }
    
    .hero-title {
        margin-bottom: 16px;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        color: var(--text-muted);
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }
</style>

<div class='hero-padding' style='text-align: center; margin-bottom: 20px;'>
    <div class='hero-icon' style='line-height: 1;'>🎓</div>
    <h1 class='hero-title'>Stop Student Attrition Before It Happens.</h1>
    <p class='hero-subtitle'>
        EduSafe AI™ is the next-generation predictive early warning system. We empower academic advisors with explainable AI to identify at-risk students and deploy targeted interventions.
    </p>
</div>
""", unsafe_allow_html=True)

# ── Responsive CTA Buttons ───────────────────────────────────────────────────
st.markdown("""
<style>
    @media (max-width: 640px) {
        .cta-container {
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 40px;
        }
    }
    
    @media (min-width: 641px) {
        .cta-container {
            display: flex;
            flex-direction: row;
            gap: 16px;
            justify-content: center;
            margin-bottom: 40px;
            flex-wrap: wrap;
        }
    }
</style>

<div class='cta-container'>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🚀 Run Live Diagnostics", type="primary", use_container_width=True, key="cta_diagnostics"):
        st.switch_page("views/input_form.py")
with col2:
    if st.button("📖 Documentation", type="secondary", use_container_width=True, key="cta_docs"):
        st.info("📚 Complete technical documentation and API reference coming soon.")

st.markdown("</div>", unsafe_allow_html=True)

# ── How It Works Section ──────────────────────────────────────────────────────
st.markdown("""
<style>
    .how-it-works-container {
        margin: 60px 0 40px 0;
    }
    
    .how-it-works-title {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 40px;
        background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .process-cards-grid {
        display: grid;
        gap: 20px;
        margin-bottom: 40px;
    }
    
    @media (max-width: 640px) {
        .process-cards-grid {
            grid-template-columns: 1fr;
            gap: 16px;
        }
        .icon-box {
            width: 56px !important;
            height: 56px !important;
        }
        .icon-box svg {
            width: 28px !important;
            height: 28px !important;
        }
    }
    
    @media (min-width: 641px) and (max-width: 1024px) {
        .process-cards-grid {
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
    }
    
    @media (min-width: 1025px) {
        .process-cards-grid {
            grid-template-columns: 1fr 1fr 1fr;
            gap: 24px;
        }
    }
    
    .process-card {
        position: relative;
        overflow: hidden;
    }
    
    .process-card:hover {
        transform: translateY(-8px);
    }
    
    .icon-box {
        width: 64px;
        height: 64px;
        margin: 0 auto 16px;
        border-radius: 18px;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 8px 20px rgba(59,130,246,0.2);
        transition: all 0.3s ease;
    }
    
    .process-card:hover .icon-box {
        transform: scale(1.1);
        box-shadow: 0 12px 30px rgba(59,130,246,0.35);
    }
    
    .process-title {
        color: var(--text-main);
        margin: 16px 0 12px 0;
        font-weight: 600;
        font-size: 18px;
    }
    
    .process-description {
        color: var(--text-muted);
        font-size: 14px;
        margin: 0;
        line-height: 1.5;
    }
</style>

<div class='how-it-works-container'>
    <div class='how-it-works-title'>🔄 How It Works</div>
    <div class='process-cards-grid'>
""", unsafe_allow_html=True)

# ── Step 1: Data Intake
st.markdown("""
        <div class="premium-card process-card">
            <div class="icon-box" style="background: linear-gradient(135deg, #1E3A5F, #3B82F6);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <ellipse cx="12" cy="5" rx="9" ry="3" stroke="#93C5FD" stroke-width="1.5"/>
                    <path d="M3 5v5c0 1.657 4.029 3 9 3s9-1.343 9-3V5" stroke="#93C5FD" stroke-width="1.5"/>
                    <path d="M3 10v5c0 1.657 4.029 3 9 3s9-1.343 9-3v-5" stroke="#93C5FD" stroke-width="1.5"/>
                </svg>
            </div>
            <h3 class="process-title">📥 Data Intake</h3>
            <p class="process-description">We ingest LMS engagement metrics, demographic proxies, and historical GPA data in real-time.</p>
        </div>
""", unsafe_allow_html=True)

# ── Step 2: AI Inference
st.markdown("""
        <div class="premium-card process-card">
            <div class="icon-box" style="background: linear-gradient(135deg, #2E1065, #8B5CF6);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <rect x="4" y="4" width="16" height="16" rx="2" stroke="#C4B5FD" stroke-width="1.5"/>
                    <path d="M9 9h6M9 12h6M9 15h4" stroke="#C4B5FD" stroke-width="1.5" stroke-linecap="round"/>
                    <circle cx="7" cy="9" r="1" fill="#C4B5FD"/>
                    <circle cx="7" cy="12" r="1" fill="#C4B5FD"/>
                    <circle cx="7" cy="15" r="1" fill="#C4B5FD"/>
                </svg>
            </div>
            <h3 class="process-title">🧠 AI Inference</h3>
            <p class="process-description">Ensemble models (Random Forest & XGBoost) analyze behavioural datapoints in milliseconds.</p>
        </div>
""", unsafe_allow_html=True)

# ── Step 3: Action Plan
st.markdown("""
        <div class="premium-card process-card">
            <div class="icon-box" style="background: linear-gradient(135deg, #052E16, #10B981);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="9" stroke="#6EE7B7" stroke-width="1.5"/>
                    <circle cx="12" cy="12" r="4" stroke="#6EE7B7" stroke-width="1.5"/>
                    <circle cx="12" cy="12" r="1" fill="#6EE7B7"/>
                    <path d="M12 2v3M12 19v3M2 12h3M19 12h3" stroke="#6EE7B7" stroke-width="1.5" stroke-linecap="round"/>
                </svg>
            </div>
            <h3 class="process-title">🎯 Prescriptive Action</h3>
            <p class="process-description">SHAP & LIME explain why a student is at risk, recommending optimal intervention plans.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Platform Impact Section ──────────────────────────────────────────────────
st.markdown("""
<style>
    .impact-container {
        margin: 60px 0 40px 0;
    }
    
    .impact-title {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 40px;
        background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metrics-grid {
        display: grid;
        gap: 20px;
        margin-bottom: 60px;
    }
    
    @media (max-width: 640px) {
        .metrics-grid {
            grid-template-columns: 1fr;
            gap: 16px;
        }
        .metric-value {
            font-size: 36px !important;
        }
        .metric-label {
            font-size: 12px !important;
        }
    }
    
    @media (min-width: 641px) and (max-width: 1024px) {
        .metrics-grid {
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }
    }
    
    @media (min-width: 1025px) {
        .metrics-grid {
            grid-template-columns: 1fr 1fr 1fr;
            gap: 24px;
        }
    }
    
    .metric-card {
        text-align: center;
        padding: 32px 20px;
        border-radius: 16px;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px rgba(59, 130, 246, 0.15);
    }
    
    .metric-value {
        font-size: 48px;
        font-weight: 800;
        margin: 0 0 12px 0;
        background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .metric-label {
        color: var(--text-muted);
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 0;
        font-size: 13px;
    }
</style>

<div class='impact-container'>
    <div class='impact-title'>📈 Platform Impact</div>
    <div class='metrics-grid'>
        <div class='metric-card premium-card'>
            <h1 class='metric-value'>94%</h1>
            <p class='metric-label'>Prediction Accuracy</p>
        </div>
        <div class='metric-card premium-card'>
            <h1 class='metric-value'>50ms</h1>
            <p class='metric-label'>Live Inference Time</p>
        </div>
        <div class='metric-card premium-card'>
            <h1 class='metric-value'>10+</h1>
            <p class='metric-label'>Explainable Features</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Features Showcase ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .features-container {
        margin: 60px 0 40px 0;
    }
    
    .features-title {
        text-align: center;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 40px;
        background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .features-grid {
        display: grid;
        gap: 16px;
        margin-bottom: 40px;
    }
    
    @media (max-width: 640px) {
        .features-grid {
            grid-template-columns: 1fr;
        }
    }
    
    @media (min-width: 641px) and (max-width: 1024px) {
        .features-grid {
            grid-template-columns: 1fr 1fr;
        }
    }
    
    @media (min-width: 1025px) {
        .features-grid {
            grid-template-columns: 1fr 1fr;
        }
    }
    
    .feature-item {
        padding: 20px;
        border-left: 4px solid #3B82F6;
        background: rgba(59, 130, 246, 0.05);
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    
    .feature-item:hover {
        border-left-color: #8B5CF6;
        background: rgba(139, 92, 246, 0.08);
        transform: translateX(4px);
    }
    
    .feature-emoji {
        font-size: 24px;
        margin-right: 10px;
    }
    
    .feature-title {
        font-weight: 600;
        color: var(--text-main);
        margin: 0 0 4px 0;
        display: inline;
    }
    
    .feature-description {
        color: var(--text-muted);
        font-size: 13px;
        margin: 0;
    }
</style>

<div class='features-container'>
    <div class='features-title'>✨ Key Features</div>
    <div class='features-grid'>
        <div class='feature-item'>
            <span class='feature-emoji'>🔍</span>
            <p class='feature-title'>Real-Time Explainability</p>
            <p class='feature-description'>Understand exactly why each prediction is made using SHAP and LIME interpretability engines.</p>
        </div>
        <div class='feature-item'>
            <span class='feature-emoji'>⚡</span>
            <p class='feature-title'>Lightning-Fast Inference</p>
            <p class='feature-description'>Get predictions in 50ms or less. Instant insights for every student interaction.</p>
        </div>
        <div class='feature-item'>
            <span class='feature-emoji'>🎯</span>
            <p class='feature-title'>Personalized Interventions</p>
            <p class='feature-description'>Receive AI-driven recommendations tailored to each student's unique risk profile.</p>
        </div>
        <div class='feature-item'>
            <span class='feature-emoji'>📊</span>
            <p class='feature-title'>Multi-Model Ensemble</p>
            <p class='feature-description'>Robust predictions from Random Forest and XGBoost working together for accuracy.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .footer-container {
        text-align: center;
        margin: 60px 0 0 0;
        padding-top: 20px;
        border-top: 1px solid var(--border-color);
    }
    
    .footer-text {
        color: var(--text-muted);
        font-size: 12px;
        margin: 12px 0;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 16px;
        flex-wrap: wrap;
        margin: 16px 0;
    }
    
    .footer-link {
        color: var(--accent);
        text-decoration: none;
        font-size: 13px;
        transition: all 0.3s ease;
    }
    
    .footer-link:hover {
        text-decoration: underline;
        color: #A78BFA;
    }
</style>

<div class='footer-container'>
    <p class='footer-text'>&copy; 2026 EduSafe AI™. All rights reserved.</p>
    <div class='footer-links'>
        <a href='#' class='footer-link'>Privacy Policy</a>
        <a href='#' class='footer-link'>Terms of Service</a>
        <a href='#' class='footer-link'>Documentation</a>
        <a href='#' class='footer-link'>GitHub</a>
    </div>
    <p class='footer-text'>Powered by ensemble ML models and explainable AI</p>
</div>
""", unsafe_allow_html=True)
