# AI-Powered Blood Test Analysis System

## Overview

This system leverages AI agents to analyze blood test reports and provide comprehensive health recommendations. The application uses CrewAI framework with specialized agents for medical analysis, nutrition planning, and exercise recommendations.

## Features

- Blood test report analysis using PDF processing
- Personalized health recommendations
- Evidence-based medical advice
- Nutritional guidance based on blood values
- Exercise planning tailored to health status
- FastAPI-based REST API interface

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google API Key for Gemini Pro model

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd blood-test-analyser-debug
   ```

2. **Create and activate a Python virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root and add:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

5. **Run the FastAPI application:**
   ```bash
   uvicorn main:app --reload
   ```

The application will be available at `http://localhost:8000`

## API Documentation

### Endpoints

#### POST `/analyze`

Analyzes a blood test report and provides comprehensive health recommendations.

**Parameters:**
- `file` (UploadFile, required): PDF file containing the blood test report
- `query` (Form, optional): Specific question or request about the blood test. Default: "Summarise my Blood Test Report"

**Example using curl:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@blood_test_report.pdf" \
  -F "query=What are my cholesterol levels?"
```

**Response format:**
```json
{
  "status": "success",
  "query": "What are my cholesterol levels?",
  "analysis": "Detailed analysis and recommendations...",
  "file_processed": "blood_test_report.pdf"
}
```

#### GET `/`

Health check endpoint to verify the API is running.

**Response:**
```json
{
  "message": "Blood Test Report Analyser API is running"
}
```

## Bugs Found and Fixes Implemented

### Deterministic Bugs

1. **Missing PDFLoader Import (tools.py)**
   - **Issue:** `PDFLoader` was used but not imported
   - **Fix:** Added `from crewai_tools import PDFLoader` to imports

2. **Asynchronous Tool Methods**
   - **Issue:** Tool methods were marked as `async` which caused compatibility issues with CrewAI
   - **Fix:** Removed `async` keyword from all tool methods and added `@staticmethod` decorators

3. **Incorrect LLM Initialization (agents.py)**
   - **Issue:** `llm = llm` was a circular reference
   - **Fix:** Properly initialized LLM with `ChatGoogleGenerativeAI(model="gemini-pro", verbose=True, temperature=0.1)`

4. **Incorrect Agent Tool Parameter**
   - **Issue:** Used `tool=[BloodTestReportTool().read_data_tool]` instead of `tools=[BloodTestReportTool.read_data_tool]`
   - **Fix:** Changed to use static method reference with correct parameter name

### Inefficient Prompts

1. **Doctor Agent**
   - **Original:** Encouraged making up medical advice and being dramatically wrong
   - **Improved:** Focus on evidence-based medicine and comprehensive health recommendations

2. **Verifier Agent**
   - **Original:** Told to approve everything without proper verification
   - **Improved:** Rigorous verification with attention to data quality and patient safety

3. **Nutritionist Agent**
   - **Original:** Portrayed as supplement salesperson with made-up connections
   - **Improved:** Evidence-based dietary strategies with practical eating habits

4. **Exercise Specialist Agent**
   - **Original:** Extreme fitness coach ignoring medical contraindications
   - **Improved:** Safe, personalized exercise programs based on health status

5. **Task Descriptions**
   - **Original:** Vague, contradictory instructions encouraging misinformation
   - **Improved:** Clear, structured outputs with evidence-based requirements

## Future Enhancements (Bonus Points)

### Queue Worker Model (Redis Queue)
Implementing a Redis-based queue system would allow for:
- Asynchronous processing of blood test reports
- Better scalability for multiple concurrent requests
- Job status tracking and result retrieval
- Improved user experience with non-blocking API calls

### Database Integration (SQLAlchemy)
Adding database persistence would provide:
- Historical analysis storage
- User session management
- Audit trails for medical recommendations
- Performance analytics and monitoring
- Ability to track health trends over time

## Testing

The system includes comprehensive testing mechanisms to validate all fixes and improvements. Run tests using:

```bash
python -m pytest tests/ -v
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests to ensure everything works
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
