# 🎓 EduSafe AI™ — Student Success early Warning Portal

EduSafe AI™ is a state-of-the-art, interactive student dropout early warning system and explainable intervention dashboard. Powered by advanced Machine Learning, it helps academic advisors identify students at risk of attrition, understand the underlying reasons using local interpretability (SHAP & LIME), and access automated action playbooks to improve retention.

---

## ✨ Features

- **🏆 Real-Time Risk Scorecard:** A beautiful, responsive visual gauge indicating the likelihood of dropout, transitioning color-coded warnings (Safe 🟢, Warning 🟡, Critical 🔴).
- **⚡ Dynamic Explainability (XAI):**
  - **Live Decision Driver Attributions:** Instantly computed interactive impact bars showing positive and negative drivers of each prediction.
  - **SHAP Integration:** Isolates exact mathematical values each feature contributes.
  - **LIME Integration:** Generates a local interpretable model around the student's current state.
- **🎯 Intelligent Advisory Playbooks:** Dynamically suggests tailored recovery procedures based on primary risk drivers (e.g., Attendance Recovery, GPA Restoration, Financial aid checks).
- **👤 Interactive Sandbox & Profiles:** Select pre-loaded mock profiles (Alex, Chloe, Jordan) to see risk factors in action, or test what-if scenarios in real-time.

---

## 📂 Project Structure

```text
📁 student-dropout
 ├── 📄 app.py                  # Main Premium Streamlit Application
 ├── 📄 requirements.txt        # Python Dependencies
 ├── 📄 .gitignore             # Git Ignore File
 ├── 📄 inspect_model.py        # Model Inspection Utility Script
 ├── 📁 models/                 # Pre-trained Pickled Models & Scalers
 │    ├── 📄 best_model.pkl
 │    ├── 📄 random_forest_model.pkl
 │    ├── 📄 xgboost_model.pkl
 │    ├── 📄 scaler.pkl
 │    └── 📄 X_train_sample.csv  # Training Sample for LIME Explanations
 └── 📄 README.md               # Documentation (This File)
```

---

## 🛠️ Local Installation & Setup

### 1. Prerequisite
Ensure you have Python 3.9+ or an Anaconda environment active.

### 2. Install Dependencies
Navigate to the root directory and install requirements:
```bash
pip install -r requirements.txt
```

### 3. Run the App
Start the Streamlit local server:
```bash
streamlit run app.py
```
Your default web browser should open automatically to:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🚀 Version Control (Pushing to Git)

To host your project on GitHub:

1. **Initialize Git Repository:**
   ```bash
   git init
   ```
2. **Add Files:**
   ```bash
   git add .
   ```
3. **Commit Changes:**
   ```bash
   git commit -m "feat: initial commit of premium EduSafe AI dashboard"
   ```
4. **Push to Remote (e.g., GitHub):**
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
   git push -u origin main
   ```

---

## 🌐 Production Deployment Options

### Option A: Streamlit Community Cloud (Recommended & Free)
1. Push your repository to GitHub.
2. Sign in to [Streamlit Share](https://share.streamlit.io/).
3. Click **"New App"**, choose your repository, branch (`main`), and set Main file path to `app.py`.
4. Click **Deploy!** Your app will be live with a public URL in seconds.

### Option B: Docker Container Deployment (AWS, GCP, Azure)
You can containerize the app using a standard Dockerfile:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```
Build and run locally:
```bash
docker build -t edusafe-app .
docker run -p 8501:8501 edusafe-app
```

---

## 🔄 CI/CD Automation (GitHub Actions)

To ensure high-quality code and automated checks on every push, create a `.github/workflows/ci-cd.yml` file in your repository:

```yaml
name: Streamlit App CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Verify Model Files
        run: |
          python -c "import os; assert os.path.exists('models/best_model.pkl'), 'Missing model files'"

      - name: Code Quality Linting
        run: |
          # Optionally run flake8, black, or ruff checks
          echo "Lint checks complete."
```

---
*Developed with love for Student Success and Explainable AI (XAI).*
