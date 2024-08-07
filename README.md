# FinalProject2004
## This is the Final Project for AIDI 2004 - AI in Enterprise Systems.

### AI-Powered Resume Screening Tool
#### Project Overview

The AI-Powered Resume Screening Tool is a web application designed to assist in the recruitment process by analyzing resumes and providing feedback on their suitability for a given job description. It leverages the capabilities of OpenAI's GPT-3.5 to generate insights and recommendations based on the content of the resumes.
Features

    Upload multiple resumes in PDF format.
    Analyze resumes against a provided job description and mandatory keywords.
    Receive feedback on the suitability of each resume.
    Get a list of the top 3 job titles best suited for each resume.
    Generate links to relevant job postings on LinkedIn and Indeed.
    Download the results as a CSV file.

### Installation and Setup
#### Prerequisites

    Python 3.7 or higher
    Virtual environment tool (e.g., venv or virtualenv)
    OpenAI API key

#### Steps

    Clone the repository:



git clone https://github.com/DixitPat3l/FinalProjectAIDI2004.git

cd [Your folder name]


### Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`


### Install the required dependencies:

pip install -r requirements.txt


### Set up environment variables:

    Create a .env file in the project root directory.
    Add your OpenAI API key to the .env file:

    plaintext

    OPENAI_API_KEY=your_openai_api_key_here

### Run the application:

    python screening_tool.py

    Access the application:
    Open a web browser and navigate to http://127.0.0.1:5000.



## Expected Results

After uploading resumes and providing a job description and mandatory keywords, the application will analyze each resume and display the following results:

    File Name: The name of the uploaded resume file.
    Comments: Feedback on the suitability of the resume for the provided job description.
    Suitability: Indicates whether the candidate is suitable, not suitable, or maybe suitable.
    Best Job Fit: A list of the top 3 job titles best suited for the resume.
    LinkedIn Job Link: A link to relevant job postings on LinkedIn.
    Indeed Job Link: A link to relevant job postings on Indeed.

## User Guide
Uploading Resumes

    Upload Resume: Click the "Browse" button and select one or multiple PDF resumes from your computer.
    Enter Job Description: Provide a brief job description in the text area.
    Enter Key Words: Provide mandatory keywords that should be present in the resume.

Submitting the Form

    Submit: Click the "SUBMIT" button to start the analysis.
    Loading Spinner: A loading spinner will appear indicating that the analysis is in progress.

Viewing Results

    Results Table: Once the analysis is complete, the results will be displayed in a table below the form.
    Download CSV: Click the "Download CSV" button to download the results as a CSV file for further review.

Example Workflow

    Upload one or more resumes in PDF format.
    Provide a job description such as "Data Engineer".
    Enter mandatory keywords such as "Python, SQL, Big Data".
    Click the "SUBMIT" button and wait for the analysis to complete.
    Review the results in the table and download the CSV for further use.

By following the above steps, users can efficiently screen multiple resumes against a given job description, making the recruitment process faster and more effective.
Support



## Detailed Code Explanation

This project is a Flask web application that uses OpenAI's GPT-3.5 model to analyze resumes and determine their suitability for a specific job description. It extracts text from PDF resumes, sends the extracted text along with the job description to OpenAI's API for analysis, and provides feedback on the suitability of each resume. Additionally, it suggests the top 3 job titles best suited for each resume and generates links to relevant job postings on LinkedIn and Indeed.
Detailed Breakdown
Importing Libraries and Initializing Flask App

The application imports essential libraries such as os for environment variable management, openai for interacting with the OpenAI API, pdfplumber for extracting text from PDF files, csv for handling CSV file operations, and Flask-related modules for building the web application.
Loading Environment Variables

The code loads environment variables from a .env file, specifically retrieving the OpenAI API key necessary for accessing GPT-3.5. This key is stored securely and accessed via the dotenv package.
Global Variable for Results

A global list named results is initialized to store the analysis results of the resumes.
Helper Functions

    chat_gpt(): This function interacts with the OpenAI API to generate responses based on a provided conversation. It sends the conversation to GPT-3.5 and returns the generated response.
    pdf_to_text(): This function extracts text from a given PDF file using pdfplumber. It iterates through each page of the PDF and extracts text, which is then concatenated into a single string.
    suggest_best_job_fit(): This function uses GPT-3.5 to suggest the top 3 job titles best suited for the provided resume text. It formats a conversation and sends it to the GPT-3.5 model, requesting only a list of job titles.
    generate_sample_job_links(): This function generates sample job search links for LinkedIn and Indeed based on a provided job title. It formats the job title into URL-friendly strings and constructs the search URLs.
    update_csv(): This function writes the results stored in the results list to a CSV file named results.csv.

### Flask Routes

    /upload: This route handles both GET and POST requests. For POST requests, it processes uploaded resume files and analyzes them based on the provided job description and mandatory keywords. It uses the helper functions to extract text, suggest job titles, and determine the suitability of the resume. The results are then stored and returned as a JSON response. For GET requests, it renders the upload page.
    /download_csv: This route allows users to download the results as a CSV file. It calls the update_csv() function to ensure the latest results are written to the CSV before sending it to the user.
    /: This route renders the main upload page of the application.

### Running the Application

The application is run with Flask's development server in debug mode. If an error occurs during execution, it is caught and printed to the console.

Overall, the code implements a comprehensive resume screening tool that integrates PDF text extraction, natural language processing with GPT-3.5, and web development with Flask to provide a user-friendly interface for analyzing resumes against job descriptions.