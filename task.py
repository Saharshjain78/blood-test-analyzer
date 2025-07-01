## Importing libraries and files
from crewai import Task

from agents import doctor, verifier
from tools import BloodTestReportTool

# Create tool instance
pdf_tool = BloodTestReportTool()

## Creating a task to help solve user's query
help_patients = Task(
    description="Analyze the user's query and the provided blood test report. Use the BloodTestReportTool to read the PDF file at {file_path}. Synthesize the information to provide a comprehensive, clear, and actionable health summary and recommendations. Prioritize evidence-based advice and identify any significant abnormalities that require attention. Include relevant health recommendations and, if appropriate, reliable external resources. User query: {query}",

    expected_output="""A well-structured report containing:
- A concise summary of the key findings from the blood test report.
- Identification of any abnormal values and their potential implications.
- Personalized health recommendations (diet, exercise, lifestyle) supported by scientific evidence.
- Suggestions for further medical consultation if necessary.
- A list of reputable sources for additional information.""",

    agent=doctor,
    tools=[pdf_tool],
    async_execution=False,
)

## Creating a nutrition analysis task
nutrition_analysis = Task(
    description="Based on the provided blood test report at {file_path}, analyze relevant blood values (e.g., glucose, cholesterol, vitamins, minerals) and formulate specific, tailored nutritional recommendations. Use the BloodTestReportTool to read the file. Consider the user's query and general dietary principles. User query: {query}",

    expected_output="""A detailed nutrition plan that includes:
- Specific dietary adjustments based on blood report findings.
- Recommendations for foods to emphasize or avoid.
- Advice on nutrient intake to address any deficiencies or imbalances.
- General healthy eating guidelines.""",

    agent=doctor,
    tools=[pdf_tool],
    async_execution=False,
)

## Creating an exercise planning task
exercise_planning = Task(
    description="Using the blood test report at {file_path} as a reference, design a safe and effective exercise plan. Use the BloodTestReportTool to read the file. Take into account any health conditions or limitations indicated by the report and the user's query. The plan should be realistic and progressive. User query: {query}",

    expected_output="""A structured exercise plan with:
- Recommended types of exercise (cardiovascular, strength, flexibility).
- Suggested intensity, duration, and frequency.
- Considerations for any health limitations from the blood report.
- A phased approach for progression.
- General safety guidelines for physical activity.""",

    agent=doctor,
    tools=[pdf_tool],
    async_execution=False,
)

    
verification = Task(
    description="Thoroughly examine the uploaded file at {file_path} to confirm it is indeed a valid blood test report. Use the BloodTestReportTool to read the file. Verify its structure, content, and the presence of expected medical parameters. Flag any anomalies or if the file is not a blood report.",

    expected_output="A clear verification status indicating whether the file is a valid blood test report. If valid, confirm its readability and relevance. If not, state the reason and suggest the appropriate file type. Include details like 'File confirmed as valid blood test report: [filename]' or 'File not a valid blood test report: [reason]'.",

    agent=doctor,
    tools=[pdf_tool],
    async_execution=False
)