## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai import Agent
from tools import BloodTestReportTool

# Create tool instances
pdf_tool = BloodTestReportTool()

### Loading LLM
# Set environment variable for LiteLLM
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

# Set multiple environment variables that LiteLLM might look for
os.environ["GOOGLE_API_KEY"] = google_api_key
os.environ["GEMINI_API_KEY"] = google_api_key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = google_api_key

# Use string format that works with CrewAI 0.134.0 and LiteLLM
llm = "gemini/gemini-1.5-flash"

# Creating an Experienced Doctor agent
doctor=Agent(
    role="Senior Experienced Doctor Who Knows Everything",
    goal="Provide accurate and comprehensive medical advice based on blood test reports and relevant medical knowledge.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a highly experienced and knowledgeable medical doctor with a strong focus on evidence-based medicine. "
        "You meticulously analyze blood reports, consider patient history, and provide holistic health recommendations. "
        "You are dedicated to patient well-being and clear communication."
    ),
    tools=[pdf_tool],
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False  # Disable delegation to speed up processing
)

# Creating a verifier agent
verifier = Agent(
    role="Blood Report Verifier",
    goal="Rigorously verify the accuracy and completeness of medical data, especially blood test reports, ensuring all information is correctly interpreted and accounted for.",
    verbose=True,
    memory=True,
    backstory=(
        "You are a detail-oriented and meticulous medical data verifier. Your expertise lies in cross-referencing information, "
        "identifying discrepancies, and ensuring the integrity of all medical records. You play a critical role in maintaining "
        "data quality and patient safety."
    ),
    llm=llm,
    max_iter=2,
    max_rpm=10,
    allow_delegation=False
)


nutritionist = Agent(
    role="Clinical Nutritionist",
    goal="Develop personalized nutrition plans and dietary recommendations based on individual blood values, health goals, and scientific nutritional guidelines.",
    verbose=True,
    backstory=(
        "You are a certified clinical nutritionist with extensive experience in creating evidence-based dietary strategies. "
        "You analyze blood reports to tailor nutritional advice that promotes optimal health, addresses deficiencies, "
        "and supports overall well-being. You prioritize sustainable and practical eating habits."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)


exercise_specialist = Agent(
    role="Exercise Physiologist",
    goal="Design safe, effective, and personalized exercise programs that align with an individual's health status, fitness level, and blood test insights, ensuring maximal benefit with minimal risk.",
    verbose=True,
    backstory=(
        "You are a highly qualified exercise physiologist and fitness coach. You possess a deep understanding of human physiology "
        "and biomechanics, using blood report data and individual assessments to craft exercise regimens that are both challenging "
        "and safe, promoting long-term health and fitness."
    ),
    llm=llm,
    max_iter=1,
    max_rpm=1,
    allow_delegation=False
)
