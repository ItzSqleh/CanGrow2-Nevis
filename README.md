# CanGrow2-Nevis 🚀 Nevis – Smart Career Path Navigator & Self-Growth Assistant

<p align="center">
  <img src="https://img.shields.io/badge/Made%20With-Python-blue?logo=python" alt="Python">
</p>

<p align="center">
  <img src="Assets/Nevis-Logo-White-Bg.jpg" alt="Nevis Logo" width="200">
</p>

<p align="center">
  <video width="600" controls>
    <source src="Assets/Nevis-IntroVideo.mp4" type="video/mp4">
    Your Browser Does Not Support The Video Tag .
  </video>
</p>

## ✨ About The Project

**Nevis** Is A Dual-Purpose AI-Powered Solution That Bridges The Gap Between Professional Job Matching And Personal Development.

This Project Combines Two Core Capabilities:

- 🔍 **Job Matching Engine** Based On Resume Semantics (Classification & Job Fit)
- 🧠 **Personal Growth Coach** That Maps Your Strengths, Gaps, And Learning Paths

Whether You're Seeking A Better Job Fit Or Want To Understand Yourself Deeper, Nevis Guides Your Next Step.

---

## 🧠 Why Nevis?

- 🎯 **AI-Powered Career Direction** – Classifies Your Resume And Matches It With The Most Suitable Job Roles.
- 🗺️ **Custom Roadmaps** – Offers A Skill-Building Plan Based On Real Job Descriptions.
- 💬 **Conversational Agent** – A Chatbot For Guidance, Feedback, And Exploration.
- 🔬 **NLP & ML Fusion** – Semantic Matching + Behavioral Insight + Data Visualization.

---

## 🛠️ Key Features

| Feature | Description |
|--------|-------------|
| **📄 Resume Classifier** | Uses NLP & ML To Suggest Best-Fit Roles Based On Uploaded Resume |
| **📊 Job EDA Insights** | Analyzes Job Market Requirements With Graphical Reports |
| **💬 Chatbot Agent** | Integrated Chat Interface For Suggestions And Feedback |
| **🧠 Self-Growth Module** | Discovers Personality Traits And Suggests Development Paths |
| **📈 Skill Gap Visualizer** | Highlights Missing Competencies Based On Target Role |
| **🐳 Docker Support** | Streamlined Environment For Seamless Deployment |

---

## ⚙️ System Functionality

**Nevis** Acts As An AI-Powered Companion That Guides Users Toward Smart Career Growth And Self-Awareness. Here's How It Works:

### 🧾 Input:
- Free-form Text From The User (E.g. Self-Descriptions, Goals, Skill Summaries)
- Optionally: Uploaded Resume Files (Future Extension)

### 🔄 Processing Pipeline:
1. 🧹 **Text Preprocessing**: Tokenization, Lemmatization, Stopword Removal
2. 🧠 **Feature Extraction**: TF-IDF (Initial), With Optional Transformer-Based Embedding (e.g., MiniLM)
3. 🎯 **Classification**: Personality Modeling + Skill Matching Using Trained ML Models
5. 💬 **ChatBot Assistant**: Interactive Guidance, Suggestions & Questions Via Prompt-Based Chat

### 🧾 Output:
- 🧠 Personality Insights (E.g., Analytical, Creative, Decisive)
- 📉 Skill Gap Report (What Skills Are Missing For Chosen Path)
- 🗺️ Roadmap (Suggested Learning Plan)
- 🤖 ChatBot Summary + Conversation Starter

---

## 🧰 Tech Stack & Tools

| Layer | Tools / Libraries |
|-------|--------------------|
| **🧠 NLP & ML** | `NLTK`, `spaCy`, `Scikit-learn`, `HuggingFace Transformers`, `Joblib`, `Pandas`, `NumPy` |
| **🧪 Modeling** | `TF-IDF`, `LogisticRegression`, `SVM`, `MiniLM (optional)` |
| **📊 Visualization** | `Matplotlib`, `Seaborn`, `Plotly`, `WordCloud` |
| **🖥️ UI/UX** | `Streamlit`, `FastAPI` (For Backend/API Layer) |
| **🧠 AI Assistant** | `Langchain`, `OpenAI API`, `Prompt Engineering` |
| **📦 Deployment** | `Docker`, `Docker Compose`, `GitHub Actions`, `Uvicorn` |
| **📂 Docs & Flow** | `Markdown`, `Draw.io`, `Jupyter Notebooks`, `Swagger` |

> ⚠️ Note: A Clear Architecture Between Backend (API), Frontend (Streamlit), And AI Engine Is Maintained For Modularity And Scalability.

---

## 🚀 Quick Start

> 🎥 **Watch The Demo Video**: [Nevis Intro & Demo](Assets/Nevis-IntroVideo.mp4)  
1. Clone The Repository:
```bash
git clone https://github.com/ItzSqleh/CanGrow2-Raw-Nevis.git
