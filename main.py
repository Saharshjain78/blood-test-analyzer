from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError
import threading

from crewai import Crew, Process
from agents import doctor
from task import help_patients

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Blood Test Report Analyser")

def run_crew_with_timeout(query: str, file_path: str, timeout: int = 25):
    """Run crew with timeout to prevent hanging"""
    try:
        medical_crew = Crew(
            agents=[doctor],
            tasks=[help_patients],
            process=Process.sequential,
            verbose=True
        )
        
        result = medical_crew.kickoff({'query': query, 'file_path': file_path})
        return result
    except Exception as e:
        logger.error(f"Error in crew execution: {str(e)}")
        raise e

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew with timeout protection"""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(run_crew_with_timeout, query, file_path, 25)
        try:
            result = future.result(timeout=25)  # 25 second timeout
            return result
        except FuturesTimeoutError:
            logger.error("Crew execution timed out after 25 seconds")
            return "Analysis timed out. Please try with a shorter query or simpler blood report."
        except Exception as e:
            logger.error(f"Error in crew execution: {str(e)}")
            return f"Error processing request: {str(e)}"

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    if file.content_type != 'application/pdf':
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file")
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Additional PDF validation - check file signature
        with open(file_path, 'rb') as f:
            header = f.read(4)
            if header != b'%PDF':
                raise HTTPException(status_code=400, detail="Invalid PDF file format")
        
        # Validate query
        if query=="" or query is None:
            query = "Summarise my Blood Test Report"
            
        # Process the blood report with all specialists
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        logger.error(f"Unexpected error processing blood report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as cleanup_e:
                logger.warning(f"Could not delete file {file_path}: {cleanup_e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)