## Importing libraries and files
import os
from dotenv import load_dotenv
load_dotenv()

from crewai.tools import BaseTool
from typing import Optional
from pydantic import Field

# Alternative PDF reading using PyPDF2 as fallback
try:
    import PyPDF2
    HAS_PYPDF2 = True
except ImportError:
    HAS_PYPDF2 = False
    print("Warning: PyPDF2 not available, using basic text reading")

# Create placeholder search tool
search_tool = None

## Creating custom pdf reader tool
class BloodTestReportTool(BaseTool):
    name: str = "Blood Test Report Reader"
    description: str = "Tool to read and extract text content from blood test report PDF files"
    
    def _run(self, path: str = 'data/sample.pdf') -> str:
        """Tool to read data from a pdf file from a path

        Args:
            path (str): Path of the pdf file. Defaults to 'data/sample.pdf'.

        Returns:
            str: Full Blood Test report file content
        """
        
        if not os.path.exists(path):
            return f"Error: File {path} not found"
        
        try:
            if HAS_PYPDF2:
                # Use PyPDF2 for PDF reading
                with open(path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    full_report = ""
                    
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        content = page.extract_text()
                        
                        # Clean and format the report data
                        while "\n\n" in content:
                            content = content.replace("\n\n", "\n")
                            
                        full_report += content + "\n"
                    
                    return full_report if full_report.strip() else "Error: Could not extract text from PDF"
            else:
                # Fallback: treat as text file or return placeholder
                try:
                    with open(path, 'r', encoding='utf-8') as file:
                        return file.read()
                except UnicodeDecodeError:
                    return f"Sample blood test report data from {path} (PDF reading not available - install PyPDF2 for full functionality)"
                    
        except Exception as e:
            return f"Error reading file {path}: {str(e)}"

## Creating Nutrition Analysis Tool
class NutritionTool:
    @staticmethod
    def analyze_nutrition_tool(blood_report_data):
        # Process and analyze the blood report data
        processed_data = blood_report_data
        
        # Clean up the data format
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":  # Remove double spaces
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
                
        # TODO: Implement nutrition analysis logic here
        return "Nutrition analysis functionality to be implemented"

## Creating Exercise Planning Tool
class ExerciseTool:
    @staticmethod
    def create_exercise_plan_tool(blood_report_data):        
        # TODO: Implement exercise planning logic here
        return "Exercise planning functionality to be implemented"