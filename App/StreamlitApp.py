import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as St
import plotly.express as Px
from PIL import Image
import base64
from io import BytesIO
from Models.Model import ResumeAnalyzer, LoadModelAndVectorizer, LoadData, ProcessNewResume

BasePath = r"D:\Main\Codeing\Python-Tut\PartSch-02-CanGrow-02\PartSch-CanGrow-02-FinalProject\CanGrow2-Raw-Nevis\Assets"
LogoPath = os.path.join(BasePath, "Nevis-Logo-White-Bg.jpg")
MainLogoPath = os.path.join(BasePath, "Nevis-Logo.png")
LogoMotionPath = os.path.join(BasePath, "Nevis-LogoMotion.mp4")
VideoPath = os.path.join(BasePath, "Nevis-IntroVideo.mp4")

def DisplayLogo():
    if os.path.exists(LogoPath):
        Img = Image.open(LogoPath)
        St.image(Img)
    else:
        St.error("Failed To Load Logo")

def DisplayLogoMotion():
    if os.path.exists(LogoMotionPath):
        with open(LogoMotionPath, 'rb') as VideoFile:
            VideoBytes = VideoFile.read()
            St.video(VideoBytes, start_time=0)
    else:
        St.error("Failed To Load Logo Motion")

def DisplayVideo():
    if os.path.exists(VideoPath):
        with open(VideoPath, 'rb') as VideoFile:
            VideoBytes = VideoFile.read()
            St.video(VideoBytes, start_time=0)
    else:
        St.error("Failed To Load Video")

St.set_page_config(page_icon=MainLogoPath, page_title="Nevis - Resume Analysis", layout="wide")
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

Analyzer = ResumeAnalyzer()
Analyzer.Classifier, Analyzer.Vectorizer = LoadModelAndVectorizer(Analyzer.ModelDir)
Resumes, Jobs, SkillGaps, JobSummaries = LoadData(Analyzer.OutputDir)

St.title("Nevis Resume Analysis")
St.markdown("Analyze Resumes And Explore Career Insights")

with St.sidebar:
    Page = St.radio("Navigation", ["Resume Analysis", "Skill Gaps", "Chatbot", "Project Overview"])

if Page == "Resume Analysis":
    St.header("Analyze Your Resume")
    UploadedFile = St.file_uploader("Upload Resume", type=['txt', 'pdf', 'docx', 'jpg', 'jpeg', 'png'])
    if UploadedFile:
        with St.spinner("Processing Resume"):
            Result = ProcessNewResume(UploadedFile, Analyzer, Analyzer.OutputDir)
            if 'Error' not in Result:
                St.session_state['ResumeText'] = Result['ResumeText']
                St.session_state['Suggestions'] = Result['Suggestions']
                St.session_state['TechSkills'] = Result['TechSkills']
                St.session_state['SoftSkills'] = Result['SoftSkills']
                St.session_state['MbtiType'] = Result['MbtiType']
                St.session_state['SkillGaps'] = Result['SkillGaps']
                St.session_state['DevelopmentPlan'] = Result['DevelopmentPlan']
                St.session_state['Summary'] = Result['Summary']
                St.subheader("Resume Analysis Results")
                St.markdown("Summary: " + Result['Summary'])
                St.markdown("Personality Type (MBTI): " + Result['MbtiType'].upper())
                St.markdown("Top Job Suggestions (Chart):")
                ChartData = {
                    "labels": [Job['Title'].title() for Job in Result['Suggestions']],
                    "values": [int(Job['Probability'] * 100) for Job in Result['Suggestions']]
                }
                Fig = Px.bar(x=ChartData["values"], y=ChartData["labels"], orientation='h', title="Top Job Suggestions", labels={"x": "Probability (%)", "y": "Job Titles"}, height=400)
                St.plotly_chart(Fig)
                St.markdown("Top Job Suggestions (Details):")
                for I, Job in enumerate(Result['Suggestions']):
                    St.markdown(str(I+1) + ". " + Job['Title'].title() + " (Probability: " + str(int(Job['Probability'] * 100)) + "%)")
                    St.markdown("Summary: " + Job['Summary'])
                    St.markdown("Career Roadmap:")
                    RoadmapData = Job['CareerRoadmap']
                    for Stage in RoadmapData["stages"]:
                        St.markdown("<div class='stage'>" + "Stage: " + Stage["name"] + ":<br>" +
                                    "  Skills: " + (', '.join(Stage["skills"]).title() if Stage["skills"] else 'None') + "<br>" +
                                    "  Courses: " + (', '.join(Stage["courses"]).title() if Stage["courses"] else 'None') + "</div>", unsafe_allow_html=True)
                    MissingSkills = Job['MissingSkills']
                    St.markdown("Missing Skills: " + (', '.join(MissingSkills).title() if MissingSkills else 'None'))
                    St.markdown("---")
                St.markdown("Extracted Skills:")
                St.markdown("Technical: " + (', '.join(Result['TechSkills']).title() if Result['TechSkills'] else 'None'))
                St.markdown("Soft Skills: " + (', '.join(Result['SoftSkills']).title() if Result['SoftSkills'] else 'None'))
                St.markdown("Personal Development Roadmap:")
                DevelopmentRoadmap = Result['Suggestions'][0]['DevelopmentRoadmap']
                for Stage in DevelopmentRoadmap["stages"]:
                    St.markdown("<div class='stage'>" + "Stage: " + Stage["name"] + ":<br>" +
                                "  Skills To Develop: " + (', '.join(Stage["skills"]).title() if Stage["skills"] else 'None') + "<br>" +
                                "  Actions: " + (', '.join(Stage["actions"]).title() if Stage["actions"] else 'None') + "</div>", unsafe_allow_html=True)
            else:
                St.error("Analysis Failed: " + Result['Error'])
    elif 'ResumeText' in St.session_state:
        St.subheader("Resume Analysis Results (Previously Uploaded)")
        Result = {
            'Summary': St.session_state['Summary'],
            'MbtiType': St.session_state['MbtiType'],
            'Suggestions': St.session_state['Suggestions'],
            'SkillGaps': St.session_state['SkillGaps'],
            'TechSkills': St.session_state['TechSkills'],
            'SoftSkills': St.session_state['SoftSkills'],
            'DevelopmentPlan': St.session_state['DevelopmentPlan']
        }
        St.markdown("Summary: " + Result['Summary'])
        St.markdown("Personality Type (MBTI): " + Result['MbtiType'].upper())
        St.markdown("Top Job Suggestions (Chart):")
        ChartData = {
            "labels": [Job['Title'].title() for Job in Result['Suggestions']],
            "values": [int(Job['Probability'] * 100) for Job in Result['Suggestions']]
        }
        Fig = Px.bar(x=ChartData["values"], y=ChartData["labels"], orientation='h', title="Top Job Suggestions", labels={"x": "Probability (%)", "y": "Job Titles"}, height=400)
        St.plotly_chart(Fig)
        St.markdown("Top Job Suggestions (Details):")
        for I, Job in enumerate(Result['Suggestions']):
            St.markdown(str(I+1) + ". " + Job['Title'].title() + " (Probability: " + str(int(Job['Probability'] * 100)) + "%)")
            St.markdown("Summary: " + Job['Summary'])
            St.markdown("Career Roadmap:")
            RoadmapData = Job['CareerRoadmap']
            for Stage in RoadmapData["stages"]:
                St.markdown("<div class='stage'>" + "Stage: " + Stage["name"] + ":<br>" +
                            "  Skills: " + (', '.join(Stage["skills"]).title() if Stage["skills"] else 'None') + "<br>" +
                            "  Courses: " + (', '.join(Stage["courses"]).title() if Stage["courses"] else 'None') + "</div>", unsafe_allow_html=True)
            MissingSkills = Job['MissingSkills']
            St.markdown("Missing Skills: " + (', '.join(MissingSkills).title() if MissingSkills else 'None'))
            St.markdown("---")
        St.markdown("Extracted Skills:")
        St.markdown("Technical: " + (', '.join(Result['TechSkills']).title() if Result['TechSkills'] else 'None'))
        St.markdown("Soft Skills: " + (', '.join(Result['SoftSkills']).title() if Result['SoftSkills'] else 'None'))
        St.markdown("Personal Development Roadmap:")
        DevelopmentRoadmap = Result['Suggestions'][0]['DevelopmentRoadmap']
        for Stage in DevelopmentRoadmap["stages"]:
            St.markdown("<div class='stage'>" + "Stage: " + Stage["name"] + ":<br>" +
                        "  Skills To Develop: " + (', '.join(Stage["skills"]).title() if Stage["skills"] else 'None') + "<br>" +
                        "  Actions: " + (', '.join(Stage["actions"]).title() if Stage["actions"] else 'None') + "</div>", unsafe_allow_html=True)
    else:
        St.warning("Please Upload A Resume To Analyze")

elif Page == "Skill Gaps":
    St.header("Skill Gaps Analysis")
    if 'SkillGaps' in St.session_state and 'Suggestions' in St.session_state:
        SkillGaps = St.session_state['SkillGaps']
        Suggestions = St.session_state['Suggestions']
        for I, (Gap, Job) in enumerate(zip(SkillGaps, Suggestions)):
            St.subheader("Job Title: " + Job['Title'].title())
            St.markdown("Required Skills: " + ', '.join(Job['RequiredSkills']).title())
            St.markdown("Missing Skills: " + (', '.join(Gap).title() if Gap else 'None'))
            St.markdown("---")
    else:
        St.warning("No Skill Gap Data Available. Analyze A Resume To Generate Skill Gaps")

elif Page == "Chatbot":
    St.header("Chatbot Assistant")
    if 'ResumeText' in St.session_state:
        ResumeText = St.session_state['ResumeText']
        MbtiType = St.session_state['MbtiType']
        Suggestions = St.session_state['Suggestions']
        UserInput = St.text_input("Ask A Question About Your Resume Or Career", placeholder="E.g., What Jobs Are Suitable? What Is My MBTI?")
        if UserInput:
            with St.spinner("Generating Response"):
                Response = Analyzer.GrokApi.ChatbotResponse(UserInput, ResumeText, MbtiType, Suggestions)
                St.markdown(Response)
        else:
            St.markdown("Ask About Jobs, Skills, MBTI, Development Paths, Or Resume Summary")
    else:
        St.warning("Please Upload And Analyze A Resume First")

elif Page == "Project Overview":
    St.header("Project Overview")
    DisplayLogo()
    St.markdown("""
        Nevis Resume Analysis Project Represents A Revolutionary Approach To Career Development And Personal Growth. This Innovative Tool Empowers Individuals To Unlock Their Full Potential By Providing Detailed Insights Into Their Professional Profiles. Through Advanced Resume Analysis, Users Can Discover Personalized Job Suggestions Tailored To Their Unique Skill Sets And Experiences.

        One Of The Core Features Of This Platform Is Its Ability To Identify Skill Gaps, Offering A Clear Roadmap To Bridge These Gaps With Targeted Development Plans. Whether You Are An Aspiring Developer, A Seasoned Manager, Or A Creative Designer, Nevis Provides Actionable Steps To Enhance Your Career Trajectory. The Integration Of Personality Insights, Such As MBTI Analysis, Adds A Layer Of Depth, Ensuring Recommendations Align With Your Natural Strengths And Preferences.
    """)
    DisplayLogoMotion()
    St.markdown("""
        Beyond Individual Growth, Nevis Aims To Foster A Community Of Lifelong Learners. The Platform Encourages Continuous Improvement By Suggesting Relevant Courses And Resources To Stay Ahead In A Competitive Job Market. Our Mission Is To Transform The Way People Approach Their Careers, Making Professional Success Accessible To All. With Real-Time Updates And A User-Friendly Interface, Nevis Stands As A Beacon Of Innovation In The Field Of Career Development.

        Launched As Part Of The CanGrow 2 Initiative By Part School, This Project Reflects A Commitment To Empowering The Next Generation Of Professionals. As We Move Forward, We Plan To Introduce Additional Features Such As Peer Reviews, Industry Trends Analysis, And Collaborative Learning Modules. Stay Tuned For More Exciting Updates As We Continue To Evolve And Expand Our Offerings.

        Join Us On This Journey To Redefine Your Career Path. Explore The Possibilities With Nevis And Take The First Step Toward Achieving Your Professional Dreams Today. Your Success Is Our Priority, And We Are Dedicated To Supporting You Every Step Of The Way.
    """)
    DisplayVideo()

St.markdown("---")
St.markdown("<div style='text-align: center; color: #455a64; font-size: 24px;'>Nevis - CanGrow 2 - Part School</div>", unsafe_allow_html=True)