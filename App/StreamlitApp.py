import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import streamlit as St
import plotly.express as Px
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
        St.error("FailedToLoadLogo")

def DisplayLogoMotion():
    if os.path.exists(LOGO_MOTION_PATH):
        with open(LOGO_MOTION_PATH, 'rb') as videoFile:
            videoBytes = videoFile.read()
            St.video(videoBytes, start_time=0)
    else:
        St.error("FailedToLoadLogoMotion")

def DisplayVideo():
    if os.path.exists(VIDEO_PATH):
        with open(VIDEO_PATH, 'rb') as videoFile:
            videoBytes = videoFile.read()
            St.video(videoBytes, start_time=0)
    else:
        St.error("FailedToLoadVideo")

St.set_page_config(page_icon=MAIN_LOGO_PATH, page_title="Nevis - ResumeAnalysis", layout="wide")
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

St.title("Nevis ResumeAnalysis")
St.markdown("AnalyzeResumesAndExploreCareerInsights")

with St.sidebar:
    page = St.radio("Navigation", ["ResumeAnalysis", "SkillGaps", "Chatbot", "ProjectOverview"])

if page == "ResumeAnalysis":
    St.header("AnalyzeYourResume")
    uploadedFile = St.file_uploader("UploadResume", type=['txt', 'pdf', 'docx', 'jpg', 'jpeg', 'png'])
    if uploadedFile:
        with St.spinner("ProcessingResume"):
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
                St.subheader("ResumeAnalysisResults")
                St.markdown("Summary: " + result['Summary'])
                St.markdown("PersonalityType (MBTI): " + result['MbtiType'].upper())
                St.markdown("TopJobSuggestions (Chart):")
                chartData = {
                    "labels": [job['Title'].title() for job in result['Suggestions']],
                    "values": [int(job['Probability'] * 100) for job in result['Suggestions']]
                }
                fig = Px.bar(x=chartData["values"], y=chartData["labels"], orientation='h', title="TopJobSuggestions", labels={"x": "Probability (%)", "y": "JobTitles"}, height=400)
                St.plotly_chart(fig)
                St.markdown("TopJobSuggestions (Details):")
                for i, job in enumerate(result['Suggestions']):
                    St.markdown(str(i+1) + ". " + job['Title'].title() + " (Probability: " + str(int(job['Probability'] * 100)) + "%)")
                    St.markdown("Summary: " + job['Summary'])
                    St.markdown("CareerRoadmap:")
                    roadmapData = job['CareerRoadmap']
                    for stage in roadmapData["stages"]:
                        St.markdown("<div class='stage'>" + "Stage: " + stage["name"] + ":<br>" +
                                    "  Skills: " + (', '.join(stage["skills"]).title() if stage["skills"] else 'None') + "<br>" +
                                    "  Courses: " + (', '.join(stage["courses"]).title() if stage["courses"] else 'None') + "</div>", unsafe_allow_html=True)
                    missingSkills = job['MissingSkills']
                    St.markdown("MissingSkills: " + (', '.join(missingSkills).title() if missingSkills else 'None'))
                    St.markdown("---")
                St.markdown("ExtractedSkills:")
                St.markdown("Technical: " + (', '.join(result['TechSkills']).title() if result['TechSkills'] else 'None'))
                St.markdown("SoftSkills: " + (', '.join(result['SoftSkills']).title() if result['SoftSkills'] else 'None'))
                St.markdown("PersonalDevelopmentRoadmap:")
                developmentRoadmap = result['Suggestions'][0]['DevelopmentRoadmap']
                for stage in developmentRoadmap["stages"]:
                    St.markdown("<div class='stage'>" + "Stage: " + stage["name"] + ":<br>" +
                                "  SkillsToDevelop: " + (', '.join(stage["skills"]).title() if stage["skills"] else 'None') + "<br>" +
                                "  Actions: " + (', '.join(stage["actions"]).title() if stage["actions"] else 'None') + "</div>", unsafe_allow_html=True)
            else:
                St.error("AnalysisFailed: " + result['Error'])
    elif 'ResumeText' in St.session_state:
        St.subheader("ResumeAnalysisResults (PreviouslyUploaded)")
        result = {
            'Summary': St.session_state['Summary'],
            'MbtiType': St.session_state['MbtiType'],
            'Suggestions': St.session_state['Suggestions'],
            'SkillGaps': St.session_state['SkillGaps'],
            'TechSkills': St.session_state['TechSkills'],
            'SoftSkills': St.session_state['SoftSkills'],
            'DevelopmentPlan': St.session_state['DevelopmentPlan']
        }
        St.markdown("Summary: " + result['Summary'])
        St.markdown("PersonalityType (MBTI): " + result['MbtiType'].upper())
        St.markdown("TopJobSuggestions (Chart):")
        chartData = {
            "labels": [job['Title'].title() for job in result['Suggestions']],
            "values": [int(job['Probability'] * 100) for job in result['Suggestions']]
        }
        fig = Px.bar(x=chartData["values"], y=chartData["labels"], orientation='h', title="TopJobSuggestions", labels={"x": "Probability (%)", "y": "JobTitles"}, height=400)
        St.plotly_chart(fig)
        St.markdown("TopJobSuggestions (Details):")
        for i, job in enumerate(result['Suggestions']):
            St.markdown(str(i+1) + ". " + job['Title'].title() + " (Probability: " + str(int(job['Probability'] * 100)) + "%)")
            St.markdown("Summary: " + job['Summary'])
            St.markdown("CareerRoadmap:")
            roadmapData = job['CareerRoadmap']
            for stage in roadmapData["stages"]:
                St.markdown("<div class='stage'>" + "Stage: " + stage["name"] + ":<br>" +
                            "  Skills: " + (', '.join(stage["skills"]).title() if stage["skills"] else 'None') + "<br>" +
                            "  Courses: " + (', '.join(stage["courses"]).title() if stage["courses"] else 'None') + "</div>", unsafe_allow_html=True)
            missingSkills = job['MissingSkills']
            St.markdown("MissingSkills: " + (', '.join(missingSkills).title() if missingSkills else 'None'))
            St.markdown("---")
        St.markdown("ExtractedSkills:")
        St.markdown("Technical: " + (', '.join(result['TechSkills']).title() if result['TechSkills'] else 'None'))
        St.markdown("SoftSkills: " + (', '.join(result['SoftSkills']).title() if result['SoftSkills'] else 'None'))
        St.markdown("PersonalDevelopmentRoadmap:")
        developmentRoadmap = result['Suggestions'][0]['DevelopmentRoadmap']
        for stage in developmentRoadmap["stages"]:
            St.markdown("<div class='stage'>" + "Stage: " + stage["name"] + ":<br>" +
                        "  SkillsToDevelop: " + (', '.join(stage["skills"]).title() if stage["skills"] else 'None') + "<br>" +
                        "  Actions: " + (', '.join(stage["actions"]).title() if stage["actions"] else 'None') + "</div>", unsafe_allow_html=True)
    else:
        St.warning("PleaseUploadAResumeToAnalyze")

elif page == "SkillGaps":
    St.header("SkillGapsAnalysis")
    if 'SkillGaps' in St.session_state and 'Suggestions' in St.session_state:
        skillGaps = St.session_state['SkillGaps']
        suggestions = St.session_state['Suggestions']
        for i, (gap, job) in enumerate(zip(skillGaps, suggestions)):
            St.subheader("JobTitle: " + job['Title'].title())
            St.markdown("RequiredSkills: " + ', '.join(job['RequiredSkills']).title())
            St.markdown("MissingSkills: " + (', '.join(gap).title() if gap else 'None'))
            St.markdown("---")
    else:
        St.warning("NoSkillGapDataAvailable.AnalyzeAResumeToGenerateSkillGaps")

elif page == "Chatbot":
    St.header("ChatbotAssistant")
    if 'ResumeText' in St.session_state:
        resumeText = St.session_state['ResumeText']
        mbtiType = St.session_state['MbtiType']
        suggestions = St.session_state['Suggestions']
        userInput = St.text_input("AskAQuestionAboutYourResumeOrCareer", placeholder="E.g., WhatJobsAreSuitable? WhatIsMyMBTI?")
        if userInput:
            with St.spinner("GeneratingResponse"):
                response = analyzer.GrokApi.ChatbotResponse(userInput, resumeText, mbtiType, suggestions)
                St.markdown(response)
        else:
            St.markdown("AskAboutJobs, Skills, MBTI, DevelopmentPaths, OrResumeSummary")
    else:
        St.warning("PleaseUploadAndAnalyzeAResumeFirst")

elif page == "ProjectOverview":
    St.header("ProjectOverview")
    DisplayLogo()
    St.markdown("""
        NevisResumeAnalysisProjectRepresentsARevolutionaryApproachToCareerDevelopmentAndPersonalGrowth. ThisInnovativeToolEmpowersIndividualsToUnlockTheirFullPotentialByProvidingDetailedInsightsIntoTheirProfessionalProfiles. ThroughAdvancedResumeAnalysis, UsersCanDiscoverPersonalizedJobSuggestionsTailoredToTheirUniqueSkillSetsAndExperiences.

        OneOfTheCoreFeaturesOfThisPlatformIsItsAbilityToIdentifySkillGaps, OfferingAClearRoadmapToBridgeTheseGapsWithTargetedDevelopmentPlans. WhetherYouAreAnAspiringDeveloper, ASeasonedManager, OrACreativeDesigner, NevisProvidesActionableStepsToEnhanceYourCareerTrajectory. TheIntegrationOfPersonalityInsights, SuchAsMBTIAnalysis, AddsALayerOfDepth, EnsuringRecommendationsAlignWithYourNaturalStrengthsAndPreferences.
    """)
    DisplayLogoMotion()
    St.markdown("""
        BeyondIndividualGrowth, NevisAimsToFosterACommunityOfLifelongLearners. ThePlatformEncouragesContinuousImprovementBySuggestingRelevantCoursesAndResourcesToStayAheadInACompetitiveJobMarket. OurMissionIsToTransformTheWayPeopleApproachTheirCareers, MakingProfessionalSuccessAccessibleToAll. WithRealTimeUpdatesAndAUserFriendlyInterface, NevisStandsAsABeaconOfInnovationInTheFieldOfCareerDevelopment.

        LaunchedAsPartOfTheCanGrow2InitiativeByPartSchool, ThisProjectReflectsACommitmentToEmpoweringTheNextGenerationOfProfessionals. AsWeMoveForward, WePlanToIntroduceAdditionalFeaturesSuchAsPeerReviews, IndustryTrendsAnalysis, AndCollaborativeLearningModules. StayTunedForMoreExcitingUpdatesAsWeContinueToEvolveAndExpandOurOfferings.

        JoinUsOnThisJourneyToRedefineYourCareerPath. ExploreThePossibilitiesWithNevisAndTakeTheFirstStepTowardAchievingYourProfessionalDreamsToday. YourSuccessIsOurPriority, AndWeAreDedicatedToSupportingYouEveryStepOfTheWay.
    """)
    DisplayVideo()

St.markdown("---")
St.markdown("<div style='text-align: center; color: #455a64; font-size: 24px;'>Nevis - CanGrow2 - PartSchool</div>", unsafe_allow_html=True)