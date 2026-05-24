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
        .hero-stats {
            flex-direction: column !important;
            gap: 12px !important;
        }
        .hero-stat-item {
            font-size: 13px !important;
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
        width: 80px;
        height: 80px;
        margin: 0 auto 24px;
        background: linear-gradient(135deg, #3B82F6, #8B5CF6);
        border-radius: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
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
        margin: 0 auto 20px;
        line-height: 1.6;
    }
    
    .hero-stats {
        display: flex;
        justify-content: center;
        gap: 24px;
        flex-wrap: wrap;
        margin: 20px 0;
        padding: 16px;
        background: rgba(59, 130, 246, 0.08);
        border-radius: 12px;
    }
    
    .hero-stat-item {
        text-align: center;
        font-size: 14px;
    }
    
    .hero-stat-value {
        font-size: 24px;
        font-weight: 700;
        background: -webkit-linear-gradient(45deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-stat-label {
        color: var(--text-muted);
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 4px;
    }
</style>

<div class='hero-padding' style='text-align: center; margin-bottom: 20px;'>
    <div class='hero-icon'>
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 1L2 6V11C2 17.6 12 24 12 24S22 17.6 22 11V6L12 1Z" stroke="#93C5FD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
            <path d="M8 12L11 15L16 10" stroke="#93C5FD" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    </div>
    <h1 class='hero-title'>Stop Student Attrition Before It Happens</h1>
    <p class='hero-subtitle'>
        EduSafe AI™ is the next-generation predictive early warning system. We empower academic advisors with explainable AI to identify at-risk students and deploy targeted interventions before it's too late.
    </p>
    <div class='hero-stats'>
        <div class='hero-stat-item'>
            <div class='hero-stat-value'>94%</div>
            <div class='hero-stat-label'>Accuracy</div>
        </div>
        <div class='hero-stat-item'>
            <div class='hero-stat-value'>50ms</div>
            <div class='hero-stat-label'>Speed</div>
        </div>
        <div class='hero-stat-item'>
            <div class='hero-stat-value'>10+</div>
            <div class='hero-stat-label'>Explainable Features</div>
        </div>
    </div>
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
    if st.button("Run Live Diagnostics", type="primary", use_container_width=True, key="cta_diagnostics"):
        st.switch_page("views/input_form.py")
with col2:
    if st.button("Documentation", type="secondary", use_container_width=True, key="cta_docs"):
        st.info("Complete technical documentation and API reference coming soon.")

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
    <div class='how-it-works-title'>Process Overview</div>
    <div class='process-cards-grid'>
""", unsafe_allow_html=True)

# ── Step 1: Data Intake
st.markdown("""
        <div class="premium-card process-card">
            <div class="icon-box" style="background: linear-gradient(135deg, #1E3A5F, #3B82F6);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S16.33 8 15.5 8 14 8.67 14 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S9.33 8 8.5 8 7 8.67 7 9.5 7.67 11 8.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z" fill="#93C5FD"/>
                </svg>
            </div>
            <h3 class="process-title">Data Intake</h3>
            <p class="process-description">We ingest LMS engagement metrics, demographic proxies, and historical GPA data in real-time.</p>
        </div>
""", unsafe_allow_html=True)

# ── Step 2: AI Inference
st.markdown("""
        <div class="premium-card process-card">
            <div class="icon-box" style="background: linear-gradient(135deg, #2E1065, #8B5CF6);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z" fill="#C4B5FD"/>
                </svg>
            </div>
            <h3 class="process-title">AI Inference</h3>
            <p class="process-description">Ensemble models (Random Forest & XGBoost) analyze behavioural datapoints in milliseconds.</p>
        </div>
""", unsafe_allow_html=True)

# ── Step 3: Action Plan
st.markdown("""
        <div class="premium-card process-card">
            <div class="icon-box" style="background: linear-gradient(135deg, #052E16, #10B981);">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm3.5-9c.83 0 1.5-.67 1.5-1.5S15.33 8 14.5 8 13 8.67 13 9.5s.67 1.5 1.5 1.5zm-7 0c.83 0 1.5-.67 1.5-1.5S8.33 8 7.5 8 6 8.67 6 9.5 6.67 11 7.5 11zm3.5 6.5c2.33 0 4.31-1.46 5.11-3.5H6.89c.8 2.04 2.78 3.5 5.11 3.5z" fill="#6EE7B7"/>
                </svg>
            </div>
            <h3 class="process-title">Prescriptive Action</h3>
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
    <div class='impact-title'>Platform Impact</div>
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
    
    .feature-icon {
        display: inline-block;
        width: 32px;
        height: 32px;
        margin-right: 12px;
        vertical-align: middle;
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
    <div class='features-title'>Key Features</div>
    <div class='features-grid'>
        <div class='feature-item'>
            <svg class='feature-icon' viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="10" stroke="#60A5FA" stroke-width="1.5"/>
                <path d="M12 6v6M12 12l4 2" stroke="#60A5FA" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <p class='feature-title'>Real-Time Explainability</p>
            <p class='feature-description'>Understand exactly why each prediction is made using SHAP and LIME interpretability engines.</p>
        </div>
        <div class='feature-item'>
            <svg class='feature-icon' viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z" stroke="#60A5FA" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <p class='feature-title'>Lightning-Fast Inference</p>
            <p class='feature-description'>Get predictions in 50ms or less. Instant insights for every student interaction.</p>
        </div>
        <div class='feature-item'>
            <svg class='feature-icon' viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="9" stroke="#60A5FA" stroke-width="1.5"/>
                <path d="M12 8v4l3 2" stroke="#60A5FA" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
            <p class='feature-title'>Personalized Interventions</p>
            <p class='feature-description'>Receive AI-driven recommendations tailored to each student's unique risk profile.</p>
        </div>
        <div class='feature-item'>
            <svg class='feature-icon' viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="3" width="18" height="18" rx="2" stroke="#60A5FA" stroke-width="1.5"/>
                <path d="M3 9h18M9 3v18M15 3v18" stroke="#60A5FA" stroke-width="1.5"/>
            </svg>
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
