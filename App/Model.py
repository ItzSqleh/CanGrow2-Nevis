import pandas as Pd
import numpy as Np
import os
import json
import joblib
import base64
import warnings
import fitz
import pytesseract
import requests
from PIL import Image
from typing import Dict, List
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from io import BytesIO
from docx import Document

warnings.filterwarnings('ignore')
nltk.download(['punkt', 'stopwords', 'wordnet', 'punkt_tab'], quiet=True)

class GrokAPI:
    def __init__(Self):
        Self.ApiKey = "xai-uVcLMsgPRkmhTBaXPdkbjFvmGoV8vHwqv5drv1qMTzjwDSIcYd3J4G3ymEBMUGdzBpSIFeA9bhc1Ht5g"
        Self.ApiUrl = "https://api.x.ai/v1/generate"
        Self.CachedResponses = {}

    def GenerateCareerPath(Self, JobTitle):
        CacheKey = f"CareerPath_{JobTitle}"
        if CacheKey in Self.CachedResponses:
            return Self.CachedResponses[CacheKey]
        try:
            Payload = {
                "prompt": f"Generate A Career Path For A {JobTitle} Role With 3 Stages",
                "max_tokens": 50
            }
            Headers = {"Authorization": f"Bearer {Self.ApiKey}"}
            Response = requests.post(Self.ApiUrl, json=Payload, headers=Headers)
            if Response.status_code == 200:
                Result = Response.json()['text'].split(", ")[:3]
                Self.CachedResponses[CacheKey] = Result
                return Result
            return ['Entry-Level Role', 'Mid-Level Role', 'Senior Role']
        except requests.exceptions.ConnectionError:
            return ['Entry-Level Role', 'Mid-Level Role', 'Senior Role']

    def GeneratePersonalDevelopment(Self, MbtiType, SoftSkills, MissingSkills):
        CacheKey = f"Development_{MbtiType}_{'_'.join(SoftSkills)}_{'_'.join(MissingSkills)}"
        if CacheKey in Self.CachedResponses:
            return Self.CachedResponses[CacheKey]
        try:
            Payload = {
                "prompt": f"Generate A Detailed Personal Development Roadmap For An Individual With MBTI Type {MbtiType}, Soft Skills {', '.join(SoftSkills)}, And Missing Skills {', '.join(MissingSkills)}, Include 5 Steps",
                "max_tokens": 150
            }
            Headers = {"Authorization": f"Bearer {Self.ApiKey}"}
            Response = requests.post(Self.ApiUrl, json=Payload, headers=Headers)
            if Response.status_code == 200:
                Plan = Response.json()['text'].split(". ")[:5]
                Result = [Step.title() for Step in Plan]
                Self.CachedResponses[CacheKey] = Result
                return Result
            return ['Work On Self-Improvement', 'Seek Mentorship', 'Improve Communication', 'Develop Leadership', 'Learn Time Management']
        except requests.exceptions.ConnectionError:
            return ['Work On Self-Improvement', 'Seek Mentorship', 'Improve Communication', 'Develop Leadership', 'Learn Time Management']

    def SummarizeText(Self, Text):
        CacheKey = f"Summary_{Text[:50]}"
        if CacheKey in Self.CachedResponses:
            return Self.CachedResponses[CacheKey]
        try:
            Payload = {"prompt": f"Summarize This Text In 6 Lines: {Text}", "max_tokens": 200}
            Headers = {"Authorization": f"Bearer {Self.ApiKey}"}
            Response = requests.post(Self.ApiUrl, json=Payload, headers=Headers)
            if Response.status_code == 200:
                Result = Response.json()['text'].title().replace("\n", ". ")
                Self.CachedResponses[CacheKey] = Result
                return Result
            if "Job Title" in Text:
                return "Skilled Professional In The Relevant Field. Proficient In Key Technical And Soft Skills. Experienced In Managing Projects And Teams. Demonstrates Strong Analytical And Problem-Solving Abilities. Ready To Take On Leadership Roles. Well-Prepared For Career Advancement And Growth."
            return "Experienced Professional With A Diverse Skill Set. Strong Background In Multiple Relevant Fields. Proficient In Both Technical And Interpersonal Skills. Demonstrates Consistent Growth And Adaptability. Ready For Advanced Career Opportunities. Committed To Continuous Learning And Professional Development."
        except requests.exceptions.ConnectionError:
            if "Job Title" in Text:
                return "Skilled Professional In The Relevant Field. Proficient In Key Technical And Soft Skills. Experienced In Managing Projects And Teams. Demonstrates Strong Analytical And Problem-Solving Abilities. Ready To Take On Leadership Roles. Well-Prepared For Career Advancement And Growth."
            return "Experienced Professional With A Diverse Skill Set. Strong Background In Multiple Relevant Fields. Proficient In Both Technical And Interpersonal Skills. Demonstrates Consistent Growth And Adaptability. Ready For Advanced Career Opportunities. Committed To Continuous Learning And Professional Development."

    def ChatbotResponse(Self, UserInput, ResumeText, MbtiType, Suggestions):
        UserInput = UserInput.lower().strip()
        if 'job' in UserInput or 'career' in UserInput:
            if Suggestions:
                Response = "Here Are The Top Job Suggestions Based On Your Resume:\n"
                for Job in Suggestions:
                    Response += "- " + Job['Title'].title() + " (Probability: " + str(int(Job['Probability'] * 100)) + "%)\n  Career Path: " + ', '.join(Job['CareerPath']) + "\n"
                return Response
            return "No Job Suggestions Available"
        elif 'skill gap' in UserInput or 'missing skill' in UserInput:
            if Suggestions:
                JobTitle = Suggestions[0]['Title']
                MissingSkills = Suggestions[0]['MissingSkills']
                return "Missing Skills For " + JobTitle.title() + ": " + (', '.join(MissingSkills).title() if MissingSkills else 'None')
            return "Please Upload A Resume"
        elif 'mbti' in UserInput or 'personality' in UserInput:
            return "Your MBTI Type Is " + MbtiType
        elif 'development path' in UserInput or 'improve' in UserInput:
            return "Your Personal Development Roadmap:\n" + "\n".join("- " + Step for Step in Suggestions[0]['DevelopmentPlan'])
        elif 'summary' in UserInput or 'resume' in UserInput:
            return "Resume Summary: " + Self.SummarizeText(ResumeText)
        elif 'job summary' in UserInput:
            if Suggestions:
                Response = "Job Summaries:\n"
                for Job in Suggestions[:3]:
                    Summary = Self.SummarizeText("Job Title: " + Job['Title'] + ". Skills: " + ', '.join(Job['RequiredSkills']) + ". Career Path: " + ', '.join(Job['CareerPath']))
                    Lines = Summary.split(". ")
                    if len(Lines) > 1:
                        Response += "- " + Job['Title'].title() + ":\n  " + ". ".join(Lines[:3]).strip() + ".\n  " + ". ".join(Lines[3:]).strip() + ".\n"
                    else:
                        Response += "- " + Job['Title'].title() + ":\n  " + Summary.strip() + "\n"
                return Response
            return "No Job Summaries Available"
        return "Please Ask About Jobs, Skills, MBTI, Development Paths, Or Resume Summary"

class ResumeAnalyzer:
    def __init__(Self):
        Self.BaseDir = r"D:\Main\Codeing\Python-Tut\PartSch-02-CanGrow-02\PartSch-CanGrow-02-FinalProject\CanGrow2-Raw-Nevis"
        Self.DataDir = os.path.join(Self.BaseDir, "Src", "Data")
        Self.ModelDir = os.path.join(Self.BaseDir, "Src", "Models")
        Self.UiDir = os.path.join(Self.BaseDir, "Src", "App", "Assets", "Models")
        Self.OutputDir = os.path.join(Self.DataDir, "Processed")
        Self.ResumePath = os.path.join(Self.DataDir, "Role-Resume-Dataset.csv")
        Self.JobDescPath = os.path.join(Self.DataDir, "Job-Description-Dataset.csv")
        Self.TechSkills = {
            'Programming': ['python', 'java', 'c++', 'javascript', 'sql', 'r', 'php', 'ruby'],
            'Web': ['html', 'css', 'react', 'angular', 'vue', 'django', 'flask', 'node.js'],
            'Data': ['pandas', 'numpy', 'tensorflow', 'pytorch', 'spark', 'hadoop', 'machine learning', 'power bi'],
            'DevOps': ['docker', 'kubernetes', 'aws', 'azure', 'ci/cd', 'jenkins', 'terraform']
        }
        Self.SoftSkills = ['communication', 'teamwork', 'leadership', 'problem solving', 'adaptability', 'time management', 'creativity', 'emotional intelligence', 'conflict resolution']
        Self.MbtiRules = {
            'developer': 'INTJ', 'manager': 'ENTJ', 'analyst': 'INTP', 'engineer': 'ISTJ',
            'designer': 'ENFP', 'consultant': 'ENTP', 'specialist': 'INFJ', 'author': 'INFP'
        }
        Self.JobPaths = {
            'seo specialist': {
                'Skills': ['seo', 'content marketing', 'google analytics', 'javascript', 'keyword research', 'link building', 'digital marketing', 'web analytics'],
                'Courses': ['SEO Masterclass', 'Content Marketing Certification', 'Google Analytics Course'],
                'Steps': ['Junior SEO Specialist', 'SEO Specialist', 'Senior SEO Specialist']
            },
            'business analyst': {
                'Skills': ['python', 'sql', 'data analysis', 'machine learning', 'excel', 'business intelligence', 'requirements gathering', 'project management'],
                'Courses': ['Data Science Bootcamp', 'Business Analysis Certification', 'Excel Advanced'],
                'Steps': ['Junior Business Analyzer', 'Business Analyst', 'Senior Business Analyst']
            },
            'author': {
                'Skills': ['writing', 'editing', 'creativity', 'research', 'publishing', 'storytelling', 'grammar', 'content strategy'],
                'Courses': ['Creative Writing Workshop', 'Publishing 101', 'Storytelling Masterclass'],
                'Steps': ['Freelance Writer', 'Published Author', 'Best-Selling Author']
            },
            'developer': {
                'Skills': ['python', 'javascript', 'sql', 'html', 'css', 'git', 'software engineering'],
                'Courses': ['Python For Data Science', 'Full Stack Web Development', 'Git Basics'],
                'Steps': ['Junior Developer', 'Developer', 'Senior Developer']
            },
            'manager': {
                'Skills': ['leadership', 'project management', 'agile', 'communication', 'team building', 'risk management'],
                'Courses': ['PMP Certification', 'Agile Scrum Master', 'Leadership Training'],
                'Steps': ['Team Lead', 'Project Manager', 'Program Manager']
            },
            'designer': {
                'Skills': ['html', 'css', 'creativity', 'ui/ux design', 'photoshop', 'illustrator', 'graphic design'],
                'Courses': ['UI/UX Design Fundamentals', 'Advanced Graphic Design', 'Photoshop Basics'],
                'Steps': ['Junior Designer', 'Designer', 'Lead Designer']
            }
        }
        os.makedirs(Self.ModelDir, exist_ok=True)
        os.makedirs(Self.OutputDir, exist_ok=True)
        os.makedirs(Self.UiDir, exist_ok=True)
        Self.Vectorizer = None
        Self.Classifier = None
        Self.GrokApi = GrokAPI()

    def PreprocessText(Self, Text):
        if not isinstance(Text, str) or not Text.strip():
            return ""
        Lemmatizer = WordNetLemmatizer()
        StopWords = set(stopwords.words('english'))
        Text = Text.lower()
        Text = re.sub(r'[^a-zA-Z\s]', '', Text)
        Text = re.sub(r'\s+', ' ', Text).strip()
        Tokens = word_tokenize(Text)
        Tokens = [Lemmatizer.lemmatize(Word) for Word in Tokens if Word not in StopWords and len(Word) > 2]
        return ' '.join(Tokens)

    def ExtractSkills(Self, Text):
        if not isinstance(Text, str) or not Text.strip():
            return []
        Text = Text.lower()
        Skills = set()
        for Category, SkillList in Self.TechSkills.items():
            for Skill in SkillList:
                Pattern = rf'\b{re.escape(Skill)}\b'
                if re.search(Pattern, Text):
                    Skills.add(Skill)
        Tokens = word_tokenize(Text)
        for Word in Tokens:
            if any(Word in Sub for Sub in Self.TechSkills.values()):
                Skills.add(Word)
        return sorted(list(Skills))

    def ExtractSoftSkills(Self, Text):
        if not isinstance(Text, str) or not Text.strip():
            return []
        Text = Text.lower()
        FoundSkills = []
        for Skill in Self.SoftSkills:
            if Skill in Text:
                FoundSkills.append(Skill)
        return FoundSkills[:7]

    def ExtractMbtiFromText(Self, Text):
        if not isinstance(Text, str) or not Text.strip():
            return None
        Text = Text.upper()
        MbtiPattern = r'\b(I|E)(N|S)(T|F)(J|P)\b'
        Match = re.search(MbtiPattern, Text)
        if Match:
            return Match.group(0)
        MbtiSentencePattern = r'(?:I am a|I am|Personality is)\s*(I|E)(N|S)(T|F)(J|P)\b'
        Match = re.search(MbtiSentencePattern, Text, re.IGNORECASE)
        if Match:
            return Match.group(1) + Match.group(2) + Match.group(3) + Match.group(4)
        return None

    def InferMbtiType(Self, JobTitle):
        if not isinstance(JobTitle, str) or not JobTitle.strip():
            return "Unknown"
        JobTitle = JobTitle.lower()
        BestScore = 0
        BestMbti = "Unknown"
        for Key, Mbti in Self.MbtiRules.items():
            Score = fuzz.partial_ratio(Key, JobTitle)
            if Score > BestScore and Score > 70:
                BestScore = Score
                BestMbti = Mbti
        return BestMbti

    def SuggestJobsAndPaths(Self, ResumeText):
        if not isinstance(ResumeText, str) or not ResumeText.strip():
            return []
        ProcessedText = Self.PreprocessText(ResumeText)
        if Self.Vectorizer is None or Self.Classifier is None:
            return []
        Features = Self.Vectorizer.transform([ProcessedText])
        Probabilities = Self.Classifier.predict_proba(Features)[0]
        Classes = Self.Classifier.classes_
        TopIndices = Np.argsort(Probabilities)[-3:][::-1]
        Suggestions = []
        for Index in TopIndices:
            JobTitle = Classes[Index]
            JobKey = JobTitle.lower()
            Path = Self.JobPaths.get(JobKey, {'Skills': [], 'Courses': [], 'Steps': []})
            if not Path['Steps']:
                Path['Steps'] = Self.GrokApi.GenerateCareerPath(JobTitle)
            Summary = Self.GrokApi.SummarizeText(
                "Job Title: " + JobTitle + ". Skills: " + ', '.join(Path['Skills']) + ". Career Path: " + ', '.join(Path['Steps'])
            )
            Suggestions.append({
                'Title': JobTitle,
                'Probability': Probabilities[Index],
                'RequiredSkills': Path['Skills'],
                'Courses': Path['Courses'],
                'CareerPath': Path['Steps'],
                'Summary': Summary
            })
        return Suggestions

    def AnalyzeSkillGap(Self, ResumeText, JobTitle):
        if not isinstance(ResumeText, str) or not ResumeText.strip() or not JobTitle:
            return []
        CurrentSkills = set(Self.ExtractSkills(ResumeText) + Self.ExtractSoftSkills(ResumeText))
        JobKey = JobTitle.lower()
        RequiredSkills = set(Self.JobPaths.get(JobKey, {}).get('Skills', []))
        AdditionalSkills = {
            'seo specialist': ['technical seo', 'ppc advertising', 'content optimization', 'market research'],
            'business analyst': ['data visualization', 'stakeholder management', 'process modeling', 'statistics'],
            'author': ['literary analysis', 'copywriting', 'self-publishing', 'marketing'],
            'developer': ['debugging', 'api design', 'version control', 'testing'],
            'manager': ['budget management', 'decision making', 'coaching', 'strategy'],
            'designer': ['user testing', 'prototyping', 'color theory', 'typography'],
            'data scientist': ['machine learning', 'statistical modeling', 'data wrangling', 'deep learning'],
            'ux researcher': ['user interviews', 'usability testing', 'survey design', 'empathy mapping'],
            'product manager': ['roadmap planning', 'user stories', 'agile methodologies', 'market analysis']
        }
        MissingSkills = list(RequiredSkills.union(set(AdditionalSkills.get(JobKey, []))) - CurrentSkills)
        return MissingSkills

    def GeneratePersonalDevelopmentPath(Self, MbtiType, SoftSkills, MissingSkills):
        return Self.GrokApi.GeneratePersonalDevelopment(MbtiType, SoftSkills, MissingSkills)

    def GenerateCareerRoadmap(Self, JobTitle):
        JobKey = JobTitle.lower()
        Path = Self.JobPaths.get(JobKey, {'Skills': [], 'Courses': [], 'Steps': []})
        Roadmap = {
            "stages": [
                {"name": Path['Steps'][0], "skills": Path['Skills'][:3], "courses": Path['Courses'][:1]},
                {"name": Path['Steps'][1], "skills": Path['Skills'][3:6], "courses": Path['Courses'][1:2]},
                {"name": Path['Steps'][2], "skills": Path['Skills'][6:], "courses": Path['Courses'][2:]}
            ]
        }
        return Roadmap

    def GenerateDevelopmentRoadmap(Self, MbtiType, SoftSkills, MissingSkills):
        Roadmap = {
            "stages": [
                {"name": "Foundation", "skills": MissingSkills[:2], "actions": ["Assess Current Skills", "Set Goals"]},
                {"name": "Development", "skills": MissingSkills[2:4], "actions": ["Enroll In Courses", "Practice Regularly"]},
                {"name": "Mastery", "skills": MissingSkills[4:], "actions": ["Lead Projects", "Seek Feedback"]}
            ]
        }
        return Roadmap

def LoadModelAndVectorizer(ModelDir):
    try:
        ModelPath = os.path.join(ModelDir, 'JobClassifier.pkl')
        if os.path.exists(ModelPath):
            LoadedModel = joblib.load(ModelPath)
            return LoadedModel['Model'], LoadedModel['Vectorizer']
        return None, None
    except:
        return None, None

def LoadData(OutputDir):
    try:
        ProcessedResumePath = os.path.join(OutputDir, "ProcessedResumesWithSkills.csv")
        ProcessedJobPath = os.path.join(OutputDir, "ProcessedJobs.csv")
        SkillsOutputPath = os.path.join(OutputDir, "Skills.json")
        SummaryOutputPath = os.path.join(OutputDir, "JobSummaries.json")
        Resumes = Pd.read_csv(ProcessedResumePath) if os.path.exists(ProcessedResumePath) else Pd.DataFrame()
        Jobs = Pd.read_csv(ProcessedJobPath) if os.path.exists(ProcessedJobPath) else Pd.DataFrame()
        SkillGaps = json.load(open(SkillsOutputPath, 'r', encoding='utf-8')) if os.path.exists(SkillsOutputPath) else []
        JobSummaries = json.load(open(SummaryOutputPath, 'r', encoding='utf-8')) if os.path.exists(SummaryOutputPath) else []
        return Resumes, Jobs, SkillGaps, JobSummaries
    except:
        return Pd.DataFrame(), Pd.DataFrame(), [], []

def ExtractTextFromFile(File, TesseractPath=None):
    try:
        if not File or not hasattr(File, 'name'):
            return ""
        FileExt = os.path.splitext(File.name)[1].lower()
        if FileExt == '.pdf':
            Doc = fitz.open(stream=File.read(), filetype="pdf")
            Text = ""
            for Page in Doc:
                Text += Page.get_text()
            Doc.close()
            return Text.strip()
        elif FileExt in ['.jpg', '.jpeg', '.png']:
            if TesseractPath:
                pytesseract.pytesseract.tesseract_cmd = TesseractPath
            Img = Image.open(File)
            Text = pytesseract.image_to_string(Img)
            return Text.strip() if Text.strip() else ""
        elif FileExt == '.txt':
            return File.read().decode('utf-8').strip()
        elif FileExt == '.docx':
            Doc = Document(File)
            Text = " ".join([Paragraph.text for Paragraph in Doc.paragraphs if Paragraph.text.strip()])
            return Text.strip() if Text.strip() else ""
        return ""
    except:
        return ""

def ProcessNewResume(File, Analyzer, OutputDir):
    try:
        ResumeText = ExtractTextFromFile(File, r'C:\Program Files\Tesseract-OCR\tesseract.exe')
        if not ResumeText:
            return {"Error": "No Text Extracted From File"}
        ProcessedText = Analyzer.PreprocessText(ResumeText)
        Suggestions = Analyzer.SuggestJobsAndPaths(ResumeText)
        TechSkills = Analyzer.ExtractSkills(ResumeText)
        SoftSkills = Analyzer.ExtractSoftSkills(ResumeText)
        MbtiTypeFromText = Analyzer.ExtractMbtiFromText(ResumeText)
        MbtiType = MbtiTypeFromText if MbtiTypeFromText else Analyzer.InferMbtiType(Suggestions[0]['Title'] if Suggestions else "developer")
        SkillGaps = [Analyzer.AnalyzeSkillGap(ResumeText, Job['Title']) for Job in Suggestions]
        DevelopmentPlan = Analyzer.GeneratePersonalDevelopmentPath(MbtiType, SoftSkills, SkillGaps[0] if SkillGaps else [])
        Summary = Analyzer.GrokApi.SummarizeText(ResumeText)
        for I, Job in enumerate(Suggestions):
            Job['MissingSkills'] = SkillGaps[I]
            Job['DevelopmentPlan'] = DevelopmentPlan
            Job['CareerRoadmap'] = Analyzer.GenerateCareerRoadmap(Job['Title'])
            Job['DevelopmentRoadmap'] = Analyzer.GenerateDevelopmentRoadmap(MbtiType, SoftSkills, SkillGaps[I])
        NewEntry = Pd.DataFrame([{
            'Text': ResumeText,
            'ProcessedText': ProcessedText,
            'TechnicalSkills': TechSkills,
            'SoftSkills': SoftSkills,
            'MbtiType': MbtiType,
            'SkillGap': SkillGaps[0] if SkillGaps else [],
            'DevelopmentPath': DevelopmentPlan,
            'JobSuggestions': [Job['Title'] for Job in Suggestions]
        }])
        ProcessedResumePath = os.path.join(OutputDir, "ProcessedResumesWithSkills.csv")
        Resume = Pd.read_csv(ProcessedResumePath) if os.path.exists(ProcessedResumePath) else Pd.DataFrame()
        Resume = Pd.concat([Resume, NewEntry], ignore_index=True)
        Resume.to_csv(ProcessedResumePath, index=False)
        SkillGapsData = [
            {'JobTitle': Job['Title'], 'RequiredSkills': Job['RequiredSkills'], 'MissingSkills': Gaps}
            for Job, Gaps in zip(Suggestions, SkillGaps)
        ]
        SkillsOutputPath = os.path.join(OutputDir, "Skills.json")
        with open(SkillsOutputPath, 'w', encoding='utf-8') as F:
            json.dump(SkillGapsData, F, ensure_ascii=False, indent=4)
        return {
            'Suggestions': Suggestions,
            'TechSkills': TechSkills,
            'SoftSkills': SoftSkills,
            'MbtiType': MbtiType,
            'SkillGaps': SkillGaps,
            'DevelopmentPlan': DevelopmentPlan,
            'Summary': Summary,
            'ResumeText': ResumeText
        }
    except:
        return {"Error": "Failed To Process Resume"}