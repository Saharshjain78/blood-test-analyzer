Project To-Do List: Blood Test Analysis System Debugging
This document outlines the step-by-step actions required to fix deterministic bugs and optimize inefficient prompts within the CrewAI blood test analysis system.

1. Initial Setup & Verification
[ ] Clone the project repository.

[ ] Create a new Python virtual environment.

[ ] Install all dependencies: pip install -r requirements.txt.

[ ] Ensure GOOGLE_API_KEY is correctly set as an environment variable or loaded via a .env file.

[ ] Run the FastAPI application: uvicorn main:app --reload.

[ ] Perform initial testing of the /analyze endpoint with sample.pdf and blood_test_report.pdf to observe current behavior and identify immediate errors.

2. Deterministic Bug Fixes
2.1. tools.py - PDFLoader Import
[ ] Open tools.py.

[ ] Add the following import statement at the top of the file:

from crewai_tools import PDFLoader

2.2. tools.py - Asynchronous Tool Methods
[ ] Open tools.py.

[ ] Locate the read_data_tool method within BloodTestReportTool.

[ ] Remove the async keyword from its definition.

Before: async def read_data_tool(path='data/sample.pdf'):

After: def read_data_tool(path='data/sample.pdf'):

[ ] Locate the analyze_nutrition_tool method within NutritionTool.

[ ] Remove the async keyword from its definition.

Before: async def analyze_nutrition_tool(blood_report_data):

After: def analyze_nutrition_tool(blood_report_data):

[ ] Locate the create_exercise_plan_tool method within ExerciseTool.

[ ] Remove the async keyword from its definition.

Before: async def create_exercise_plan_tool(blood_report_data):

After: def create_exercise_plan_tool(blood_report_data):

2.3. LLM Initialization
[ ] Open agents.py.

[ ] Locate the line llm = llm.

[ ] Replace it with a proper LLM initialization. Example using langchain_google_genai:

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.1)

[ ] Remove the llm = llm line from main.py if it exists there, as the LLM should be initialized once in agents.py and imported.

2.4. agents.py - Agent Tool Parameter
[ ] Open tools.py.

[ ] Locate the read_data_tool method within BloodTestReportTool.

[ ] Add the @staticmethod decorator above its definition.

Before:

# ...
def read_data_tool(path='data/sample.pdf'):
# ...

After:

# ...
@staticmethod
def read_data_tool(path='data/sample.pdf'):
# ...

[ ] Open agents.py.

[ ] Locate the doctor agent definition.

[ ] Change tool=[BloodTestReportTool().read_data_tool] to tools=[BloodTestReportTool.read_data_tool].

Before: tool=[BloodTestReportTool().read_data_tool],

After: tools=[BloodTestReportTool.read_data_tool],

2.5. task.py - Task Tool References
[ ] Open task.py.

[ ] Verify that all tasks referencing BloodTestReportTool.read_data_tool are correctly using tools=[BloodTestReportTool.read_data_tool] (which should be correct after step 2.4).

3. Inefficient Prompt Optimization
3.1. agents.py - Agent Backstories and Goals
[ ] Open agents.py.

[ ] Doctor Agent:

[ ] Update goal: "Provide accurate and comprehensive medical advice based on blood test reports and relevant medical knowledge."

[ ] Update backstory: "You are a highly experienced and knowledgeable medical doctor with a strong focus on evidence-based medicine. You meticulously analyze blood reports, consider patient history, and provide holistic health recommendations. You are dedicated to patient well-being and clear communication."

[ ] Verifier Agent:

[ ] Update goal: "Rigorously verify the accuracy and completeness of medical data, especially blood test reports, ensuring all information is correctly interpreted and accounted for."

[ ] Update backstory: "You are a detail-oriented and meticulous medical data verifier. Your expertise lies in cross-referencing information, identifying discrepancies, and ensuring the integrity of all medical records. You play a critical role in maintaining data quality and patient safety."

[ ] Nutritionist Agent:

[ ] Update goal: "Develop personalized nutrition plans and dietary recommendations based on individual blood values, health goals, and scientific nutritional guidelines."

[ ] Update backstory: "You are a certified clinical nutritionist with extensive experience in creating evidence-based dietary strategies. You analyze blood reports to tailor nutritional advice that promotes optimal health, addresses deficiencies, and supports overall well-being. You prioritize sustainable and practical eating habits."

[ ] Exercise Specialist Agent:

[ ] Update goal: "Design safe, effective, and personalized exercise programs that align with an individual's health status, fitness level, and blood test insights, ensuring maximal benefit with minimal risk."

[ ] Update backstory: "You are a highly qualified exercise physiologist and fitness coach. You possess a deep understanding of human physiology and biomechanics, using blood report data and individual assessments to craft exercise regimens that are both challenging and safe, promoting long-term health and fitness."

3.2. task.py - Task Descriptions and Expected Outputs
[ ] Open task.py.

[ ] help_patients Task:

[ ] Update description: "Analyze the user's query and the provided blood test report. Synthesize the information to provide a comprehensive, clear, and actionable health summary and recommendations. Prioritize evidence-based advice and identify any significant abnormalities that require attention. Include relevant health recommendations and, if appropriate, reliable external resources."

[ ] Update expected_output: "A well-structured report containing:\n- A concise summary of the key findings from the blood test report.\n- Identification of any abnormal values and their potential implications.\n- Personalized health recommendations (diet, exercise, lifestyle) supported by scientific evidence.\n- Suggestions for further medical consultation if necessary.\n- A list of reputable sources for additional information."

[ ] nutrition_analysis Task:

[ ] Update description: "Based on the provided blood test report, analyze relevant blood values (e.g., glucose, cholesterol, vitamins, minerals) and formulate specific, tailored nutritional recommendations. Consider the user's query and general dietary principles."

[ ] Update expected_output: "A detailed nutrition plan that includes:\n- Specific dietary adjustments based on blood report findings.\n- Recommendations for foods to emphasize or avoid.\n- Advice on nutrient intake to address any deficiencies or imbalances.\n- General healthy eating guidelines."

[ ] exercise_planning Task:

[ ] Update description: "Using the blood test report as a reference, design a safe and effective exercise plan. Take into account any health conditions or limitations indicated by the report and the user's query. The plan should be realistic and progressive."

[ ] Update expected_output: "A structured exercise plan with:\n- Recommended types of exercise (cardiovascular, strength, flexibility).\n- Suggested intensity, duration, and frequency.\n- Considerations for any health limitations from the blood report.\n- A phased approach for progression.\n- General safety guidelines for physical activity."

[ ] verification Task:

[ ] Update description: "Thoroughly examine the uploaded file to confirm it is indeed a valid blood test report. Verify its structure, content, and the presence of expected medical parameters. Flag any anomalies or if the file is not a blood report."

[ ] Update expected_output: "A clear verification status indicating whether the file is a valid blood test report. If valid, confirm its readability and relevance. If not, state the reason and suggest the appropriate file type. Include details like 'File confirmed as valid blood test report: [filename]' or 'File not a valid blood test report: [reason]'."

4. Code Refactoring and Best Practices
4.1. main.py - Error Handling and Cleanup
[ ] Open main.py.

[ ] Locate the finally block within the analyze_blood_report function.

[ ] Modify the except block for os.remove to log the error instead of pass.

Before:

# ...
    try:
        os.remove(file_path)
    except:
        pass  # Ignore cleanup errors

After:

# ...
    try:
        os.remove(file_path)
    except Exception as cleanup_e:
        print(f"Warning: Could not delete file {file_path}: {cleanup_e}")

4.2. General Code Structure and Readability
[ ] Review all Python files (agents.py, main.py, task.py, tools.py).

[ ] Ensure consistent indentation (e.g., 4 spaces).

[ ] Add comments for complex logic, function headers, and non-obvious parts of the code.

[ ] Consider using f-strings for string formatting where appropriate.

5. README.md Documentation Update
[ ] Open README.md.

[ ] Remove the "You're All Not Set! 🐛 Debug Mode Activated!" section.

[ ] Update the document with the following sections and content:

[ ] Project Title: A clear and descriptive title (e.g., "AI-Powered Blood Test Analysis System").

[ ] Overview: A brief explanation of the system's purpose.

[ ] Features: List the key functionalities (e.g., "Blood test report analysis," "Personalized health recommendations").

[ ] Getting Started:

[ ] Instructions for cloning the repository.

[ ] Steps to create and activate a Python virtual environment.

[ ] Command to install dependencies (pip install -r requirements.txt).

[ ] Instructions on setting the GOOGLE_API_KEY environment variable.

[ ] Command to run the FastAPI application (uvicorn main:app --reload).

[ ] API Documentation:

[ ] Endpoint: /analyze (POST request).

[ ] Parameters: file (UploadFile, required), query (Form, optional).

[ ] Example usage using curl or Postman.

[ ] Description of the expected JSON response format.

[ ] Bugs Found and Fixes Implemented:

[ ] Create subsections for "Deterministic Bugs" and "Inefficient Prompts."

[ ] For each bug, describe the original issue and the specific code change made to fix it.

[ ] For prompt optimizations, show examples of the original problematic prompts and the improved versions, explaining the rationale behind the changes.

[ ] Future Enhancements (Bonus Points):

[ ] Briefly describe the Queue Worker Model (e.g., Redis Queue, Celery) and its benefits for concurrency.

[ ] Briefly describe Database Integration and its benefits for data storage and user management.
6. Bonus Point Implementation (Optional)
6.1. Queue Worker Model (e.g., Redis Queue)
[ ] Install Redis server (if not already available).

[ ] Add redis and rq to requirements.txt and install them.

[ ] Modify main.py:

[ ] Import Queue from rq.

[ ] Initialize a Redis Queue instance.

[ ] In the analyze_blood_report endpoint, instead of directly calling run_crew, enqueue the task to the Redis queue.

[ ] Return a response immediately with a job ID.

[ ] Create a new file, worker.py:

[ ] Import necessary functions (run_crew).

[ ] Set up an rq worker to listen to the queue and execute jobs.

[ ] (Optional) Implement an endpoint in main.py to check job status or retrieve results from Redis.

6.2. Database Integration (e.g., SQLite/SQLAlchemy)
[ ] Add sqlalchemy and sqlite3 (if not built-in) to requirements.txt and install them.

[ ] Define SQLAlchemy models for AnalysisResult (e.g., id, query, analysis_text, file_name, timestamp).

[ ] Initialize a database engine and session in a separate module (e.g., database.py).

[ ] Modify run_crew or create a new function to persist the analysis result to the database after successful processing.

[ ] (Optional) Implement endpoints in main.py to retrieve historical analysis results from the database.

7. Final Testing and Validation
[ ] Run the application and perform end-to-end testing with various PDF inputs (valid, invalid, different content).

[ ] Verify that all deterministic bugs are resolved and no new runtime errors are introduced.

[ ] Confirm that the AI agents provide accurate, professional, and helpful responses based on the optimized prompts.

[ ] Review the updated README.md for clarity, completeness, and accuracy.

[ ] If bonus points were implemented, test the asynchronous job submission/status and database persistence.