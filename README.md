# 📌 Nevis – CanGrow 2 – Smart Career Path Navigator & Self-Growth Assistant

<video width="600" controls>  
  <source src="Assets/Nevis-IntroVideo.mp4" type="video/mp4">  
  Your Browser Does Not Support The Video Tag.  
</video>  

## ✨ About The Project  
Nevis Is An AI-Powered Career Navigation Platform That Helps Professionals And Job Seekers:  
- 📄 Upload Resumes In Multiple Formats (TXT/PDF/Images)  
- 🔍 Receive AI-Generated Career Insights  
- 💡 Get Personalized Guidance Through Chatbot Interactions  
- 🎯 Identify Skill Gaps And Development Opportunities  

Built With Streamlit And Integrated With Trained ML Models From [CanGrow2-Raw-Nevis](https://github.com/example), This Tool Focuses On Accessibility And Actionable Career Planning.

## 🧠 Key Features  
| Feature | Description |
|---------|-------------|
| **Multi-Format Resume Parser** | Extracts Text From TXT/PDF/Image Files |
| **AI Job Matching** | Suggests Optimal Roles Using Trained Classifier |
| **Skill Gap Analyzer** | Identifies Missing Competencies For Target Roles |
| **Interactive Roadmaps** | Generates Step-By-Step Career Progression Plans |
| **Visual Analytics** | Presents Data Through Interactive Charts |
| **Dockerized Deployment** | One-Click Containerization Support |

## 🏗️ Repository Structure + Will Be Changed
CanGrow2-Final-Nevis/
├── Assets/ # Media Files
│ ├── Nevis-Logo-White-Bg.jpg
│ └── Nevis-IntroVideo.mp4
├── Src/
│ ├── App/ # Streamlit Application
│ │ ├── StreamlitApp.py # Main UI Script
│ ├── Data/ # Processed Datasets
│ │ ├── Role-Resume-Dataset.csv
│ │ └── Processed/ # Analyzed Outputs
│ └── Models/ # Trained ML Models
├── Dockerfile # Container Config
├── docker-compose.yml # Orchestration
└── requirements.txt # Python Dependencies


## 🛠️ Tech Stack  
**Core Components**  
- **Backend**: Python 3.8+  
- **ML Framework**: Scikit-learn 1.5.2  
- **NLP Toolkit**: NLTK 3.9.1  
- **Document Processing**: PyMuPDF, Pytesseract  
- **Frontend**: Streamlit 1.39.0  
- **Containerization**: Docker  

## ⚙️ Core Workflows  
1. **Resume Processing Pipeline**  
   - File Upload → Text Extraction → NLP Cleaning → Feature Generation  
2. **Job Recommendation Engine**  
   - TF-IDF Vectorization → Model Inference → Top-K Role Selection  
3. **Skill Gap Analysis**  
   - Skill Extraction → Competency Matching → Gap Visualization  
4. **Interactive Chatbot**  
   - Query Understanding → Knowledge Retrieval → Response Generation  

## 🚀 Deployment  
### Local Setup  
```bash
git clone https://github.com/ItzSqleh/CanGrow2-Final-Nevis.git
cd CanGrow2-Final-Nevis
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run Src/App/StreamlitApp.py

### Docker Deployment
```bash
docker-compose up --build
# Access at http://localhost:8501

## 📊 Expected Outputs

- **Job Recommendations :**: Ranked List With Confidence Scores  
- **Skill Reports :**: Missing/Existing Skills Matrix
- **Career Pathways :**: Timeline-Based Progression Plans
- **Chat Transcripts :**: Personalized Q&A Sessions

> 🎥 **Watch The Demo Video**: [Nevis Intro & Demo](Assets/Nevis-IntroVideo.mp4)  

> ⚠️ Note: All Output Files Are Stored In Src/Data/Processed/ Directory .
