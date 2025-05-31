import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as St
from PIL import Image
import base64
from io import BytesIO
from Model import ResumeAnalyzer, LoadModelAndVectorizer, LoadData, ProcessNewResume

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'Statics')
MODEL_DIR = os.path.join(BASE_DIR, 'Assets', 'Models')

LOGO_PATH = os.path.join(STATIC_DIR, 'Nevis-Logo-White-Bg.jpg')
MAIN_LOGO_PATH = os.path.join(STATIC_DIR, 'Nevis-Logo.png')
LOGO_MOTION_PATH = os.path.join(STATIC_DIR, 'Nevis-LogoMotion.mp4')
VIDEO_PATH = os.path.join(STATIC_DIR, 'Nevis-IntroVideo.mp4')

def DisplayLogo():
    if os.path.exists(LOGO_PATH):
        img = Image.open(LOGO_PATH)
        St.image(img)
    else:
        St.error("Failed To Load Logo 🚫")

def DisplayLogoMotion():
    if os.path.exists(LOGO_MOTION_PATH):
        with open(LOGO_MOTION_PATH, 'rb') as videoFile:
            videoBytes = videoFile.read()
            St.video(videoBytes, start_time=0)
    else:
        St.error("Failed To Load Logo Motion 🚫")

def DisplayVideo():
    if os.path.exists(VIDEO_PATH):
        with open(VIDEO_PATH, 'rb') as videoFile:
            videoBytes = videoFile.read()
            St.video(videoBytes, start_time=0)
    else:
        St.error("Failed To Load Video 🚫")

St.set_page_config(page_icon=MAIN_LOGO_PATH, page_title="Nevis - Resume Analysis", layout="wide")
St.markdown("""
<style>
    .main { background: #f5f6fa; padding: 20px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); max-width: 1200px; margin: auto; }
    .stButton>button { background-color: #1976d2; color: #ffffff; border-radius: 8px; padding: 10px 20px; font-weight: 600; font-size: 14px; border: none; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #1565c0; transform: translateY(-2px); }
    .stFileUploader { background-color: #ffffff; border: 2px dashed #b0bec5; border-radius: 8px; padding: 15px; }
    h1, h2, h3 { color: #0d47a1; font-family: 'Arial', sans-serif; font-weight: 600; }
    .sidebar .sidebar-content { background-color: #ffffff; padding: 20px; border-radius: 8px; }
    .card { background-color: #ffffff; padding: 20px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .roadmap { display: flex; flex-direction: column; gap: 10px; }
    .stage { background: #e3f2fd; padding: 15px; border-left: 4px solid #1976d2; border-radius: 5px; color: #1a237e; }
</style>
""", unsafe_allow_html=True)

analyzer = ResumeAnalyzer()
analyzer.Classifier, analyzer.Vectorizer = LoadModelAndVectorizer(MODEL_DIR)
resumes, jobs, skillGaps, jobSummaries = LoadData(os.path.join(BASE_DIR, 'Assets', 'Models'))

St.title("Nevis Resume Analysis 📄")
St.markdown("Analyze Resumes And Explore Career Insights 🚀")

with St.sidebar:
    page = St.radio("Navigation", ["ResumeAnalysis", "SkillGaps", "Chatbot", "ProjectOverview"])

if page == "ResumeAnalysis":
    St.header("Analyze Your Resume 📝")
    uploadedFile = St.file_uploader("Upload Your Resume Here", type=['txt', 'pdf', 'docx', 'jpg', 'jpeg', 'png'])
    if uploadedFile:
        with St.spinner("Processing Your Resume... ⏳"):
            result = ProcessNewResume(uploadedFile, analyzer, MODEL_DIR)
            if 'Error' not in result:
                St.session_state['ResumeText'] = result['ResumeText']
                St.session_state['Suggestions'] = result['Suggestions']
                St.session_state['TechSkills'] = result['TechSkills']
                St.session_state['SoftSkills'] = result['SoftSkills']
                St.session_state['MbtiType'] = result['MbtiType']
                St.session_state['SkillGaps'] = result['SkillGaps']
                St.session_state['DevelopmentPlan'] = result['DevelopmentPlan']
                St.session_state['Summary'] = result['Summary']
                St.subheader("Resume Analysis Results 🌟")
                St.markdown(f"**Summary:** {result['Summary']}")
                St.markdown(f"**Personality Type (Mbti):** {result['MbtiType'].upper()} 🧠")
                St.markdown("**Top Job Suggestions:** 💼")
                if result['Suggestions']:
                    for i, job in enumerate(result['Suggestions']):
                        St.markdown(f"{i+1}. {job['Title'].title()} (Probability: {int(job['Probability'] * 100)}%)")
                        St.markdown(f"**Summary:** {job['Summary']}")
                        St.markdown("**Career Roadmap:** 📈")
                        roadmapData = job['CareerRoadmap']
                        for stage in roadmapData["stages"]:
                            St.markdown("<div class='stage'>" + f"Stage: {stage['name']}:<br>" +
                                        f"  Skills: {', '.join(stage['skills']).title() if stage['skills'] else 'None'}<br>" +
                                        f"  Courses: {', '.join(stage['courses']).title() if stage['courses'] else 'None'}" + "</div>", unsafe_allow_html=True)
                        missingSkills = job['MissingSkills']
                        St.markdown(f"**Missing Skills:** {', '.join(missingSkills).title() if missingSkills else 'None'} 🚧")
                        St.markdown("---")
                else:
                    St.markdown("No Job Suggestions Available 😔")
                St.markdown("**Extracted Skills:** 🛠️")
                St.markdown(f"**Technical Skills:** {', '.join(result['TechSkills']).title() if result['TechSkills'] else 'None'} 💻")
                St.markdown(f"**Soft Skills:** {', '.join(result['SoftSkills']).title() if result['SoftSkills'] else 'None'} 🤝")
                St.markdown("**Personal Development Roadmap:** 🌱")
                if result['Suggestions'] and 'DevelopmentRoadmap' in result['Suggestions'][0]:
                    developmentRoadmap = result['Suggestions'][0]['DevelopmentRoadmap']
                    for stage in developmentRoadmap["stages"]:
                        St.markdown("<div class='stage'>" + f"Stage: {stage['name']}:<br>" +
                                    f"  Skills To Develop: {', '.join(stage['skills']).title() if stage['skills'] else 'None'}<br>" +
                                    f"  Actions: {', '.join(stage['actions']).title() if stage['actions'] else 'None'}" + "</div>", unsafe_allow_html=True)
                else:
                    St.markdown("No Development Roadmap Available 😢")
            else:
                St.error(f"Analysis Failed: {result['Error']} 🚨")
    elif 'ResumeText' in St.session_state:
        St.subheader("Resume Analysis Results (Previously Uploaded) 📂")
        result = {
            'Summary': St.session_state['Summary'],
            'MbtiType': St.session_state['MbtiType'],
            'Suggestions': St.session_state['Suggestions'],
            'SkillGaps': St.session_state['SkillGaps'],
            'TechSkills': St.session_state['TechSkills'],
            'SoftSkills': St.session_state['SoftSkills'],
            'DevelopmentPlan': St.session_state['DevelopmentPlan']
        }
        St.markdown(f"**Summary:** {result['Summary']}")
        St.markdown(f"**Personality Type (Mbti):** {result['MbtiType'].upper()} 🧠")
        St.markdown("**Top Job Suggestions:** 💼")
        if result['Suggestions']:
            for i, job in enumerate(result['Suggestions']):
                St.markdown(f"{i+1}. {job['Title'].title()} (Probability: {int(job['Probability'] * 100)}%)")
                St.markdown(f"**Summary:** {job['Summary']}")
                St.markdown("**Career Roadmap:** 📈")
                roadmapData = job['CareerRoadmap']
                for stage in roadmapData["stages"]:
                    St.markdown("<div class='stage'>" + f"Stage: {stage['name']}:<br>" +
                                f"  Skills: {', '.join(stage['skills']).title() if stage['skills'] else 'None'}<br>" +
                                f"  Courses: {', '.join(stage['courses']).title() if stage['courses'] else 'None'}" + "</div>", unsafe_allow_html=True)
                missingSkills = job['MissingSkills']
                St.markdown(f"**Missing Skills:** {', '.join(missingSkills).title() if missingSkills else 'None'} 🚧")
                St.markdown("---")
        else:
            St.markdown("No Job Suggestions Available 😔")
        St.markdown("**Extracted Skills:** 🛠️")
        St.markdown(f"**Technical Skills:** {', '.join(result['TechSkills']).title() if result['TechSkills'] else 'None'} 💻")
        St.markdown(f"**Soft Skills:** {', '.join(result['SoftSkills']).title() if result['SoftSkills'] else 'None'} 🤝")
        St.markdown("**Personal Development Roadmap:** 🌱")
        if result['Suggestions'] and 'DevelopmentRoadmap' in result['Suggestions'][0]:
            developmentRoadmap = result['Suggestions'][0]['DevelopmentRoadmap']
            for stage in developmentRoadmap["stages"]:
                St.markdown("<div class='stage'>" + f"Stage: {stage['name']}:<br>" +
                            f"  Skills To Develop: {', '.join(stage['skills']).title() if stage['skills'] else 'None'}<br>" +
                            f"  Actions: {', '.join(stage['actions']).title() if stage['actions'] else 'None'}" + "</div>", unsafe_allow_html=True)
        else:
            St.markdown("No Development Roadmap Available 😢")
    else:
        St.warning("Please Upload A Resume To Analyze 📤")

elif page == "SkillGaps":
    St.header("Skill Gaps Analysis 🔍")
    if 'SkillGaps' in St.session_state and 'Suggestions' in St.session_state:
        skillGaps = St.session_state['SkillGaps']
        suggestions = St.session_state['Suggestions']
        for i, (gap, job) in enumerate(zip(skillGaps, suggestions)):
            St.subheader(f"Job Title: {job['Title'].title()} 💼")
            St.markdown(f"**Required Skills:** {', '.join(job['RequiredSkills']).title()} ✅")
            St.markdown(f"**Missing Skills:** {', '.join(gap).title() if gap else 'None'} 🚧")
            St.markdown("---")
    else:
        St.warning("No Skill Gap Data Available. Please Analyze A Resume To Generate Skill Gaps 📊")

elif page == "Chatbot":
    St.header("Chatbot Assistant 🤖")
    if 'ResumeText' in St.session_state:
        resumeText = St.session_state['ResumeText']
        mbtiType = St.session_state['MbtiType']
        suggestions = St.session_state['Suggestions']
        userInput = St.text_input("Ask A Question About Your Resume Or Career", placeholder="E.g., What Jobs Are Suitable? What Is My Mbti?")
        if userInput:
            with St.spinner("Generating Response... ⏳"):
                response = analyzer.GrokApi.ChatbotResponse(userInput, resumeText, mbtiType, suggestions)
                St.markdown(response)
        else:
            St.markdown("Ask About Jobs, Skills, Mbti, Development Paths, Or Resume Summary 💡")
    else:
        St.warning("Please Upload And Analyze A Resume First 📤")

elif page == "ProjectOverview":
    St.header("Project Overview 🌟")
    DisplayLogo()
    St.markdown("""
        The Nevis Resume Analysis Project Represents A Revolutionary Approach To Career Development And Personal Growth. 🌱  
        This Innovative Tool Empowers Individuals To Unlock Their Full Potential By Providing Detailed Insights Into Their Professional Profiles.  
        Through Advanced Resume Analysis, Users Can Discover Personalized Job Suggestions Tailored To Their Unique Skill Sets And Experiences. 📄

        One Of The Core Features Of This Platform Is Its Ability To Identify Skill Gaps, Offering A Clear Roadmap To Bridge These Gaps With Targeted Development Plans. 📈  
        Whether You Are An Aspiring Developer, A Seasoned Manager, Or A Creative Designer, Nevis Provides Actionable Steps To Enhance Your Career Trajectory.  
        The Integration Of Personality Insights, Such As Mbti Analysis, Adds A Layer Of Depth, Ensuring Recommendations Align With Your Natural Strengths And Preferences. 🧠
    """)
    DisplayLogoMotion()
    St.markdown("""
        Beyond Individual Growth, Nevis Aims To Foster A Community Of Lifelong Learners. 🤝  
        The Platform Encourages Continuous Improvement By Suggesting Relevant Courses And Resources To Stay Ahead In A Competitive Job Market.  
        Our Mission Is To Transform The Way People Approach Their Careers, Making Professional Success Accessible To All. 🌍  
        With Real-Time Updates And A User-Friendly Interface, Nevis Stands As A Beacon Of Innovation In The Field Of Career Development. ✨

        Launched As Part Of The Cangrow2 Initiative By Partschool, This Project Reflects A Commitment To Empowering The Next Generation Of Professionals. 🚀  
        As We Move Forward, We Plan To Introduce Additional Features Such As Peer Reviews, Industry Trends Analysis, And Collaborative Learning Modules.  
        Stay Tuned For More Exciting Updates As We Continue To Evolve And Expand Our Offerings. 📅

        Join Us On This Journey To Redefine Your Career Path. Explore The Possibilities With Nevis And Take The First Step Toward Achieving Your Professional Dreams Today. 🎯  
        Your Success Is Our Priority, And We Are Dedicated To Supporting You Every Step Of The Way. 💪
    """)
    DisplayVideo()

St.markdown("---")
St.markdown("<div style='text-align: center; color: #455a64; font-size: 24px;'>Nevis - Cangrow2 - Partschool 🌟</div>", unsafe_allow_html=True)
