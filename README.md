# FinalProject2004
## This is the Final Project for AIDI 2004 - AI in Enterprise Systems.

## Team Members-
    Bhowmik Doshi (100891425)
    Dixit Patel (100893847)
    Meharan Shaikh (100896426)
    Sanchit Kalra (100901585)

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


## Detailed Code Explanation for `test_screening_tool.py`

The `test_screening_tool.py` file contains unit tests for the main application functions. These tests ensure that each component of the resume screening tool works correctly.

### Importing Libraries and Configuring Flask App for Testing

The script imports necessary libraries such as `pytest` for testing, `os` for file operations, and `fpdf` for creating PDF files. It also imports Flask and related modules for testing the web application.

### Fixtures

`@pytest.fixture`
- Defines a `client` fixture that configures the Flask app for testing. It creates a test client that can be used to simulate requests to the application.

### Helper Function

`create_test_resume_pdf(path)`
- A helper function that creates a sample PDF file with dummy resume content. This content is used to test the PDF text extraction functionality.

### Test Functions

`test_pdf_to_text()`
- This test creates a dummy PDF file using the `create_test_resume_pdf` function.
- It then tests the `pdf_to_text` function to ensure it correctly extracts text from the PDF.
- Finally, it cleans up by deleting the test PDF file.

`test_suggest_best_job_fit()`
- Tests the `suggest_best_job_fit` function to ensure it returns relevant job titles based on the provided resume text.

`test_generate_sample_job_links()`
- Tests the `generate_sample_job_links` function to ensure it correctly generates LinkedIn and Indeed job search links based on a given job title.

`test_chat_gpt()`
- Tests the `chat_gpt` function to ensure it returns appropriate responses based on a simulated conversation.

`test_upload_resume(client)`
- Creates a dummy PDF file using the `create_test_resume_pdf` function.
- Simulates uploading the PDF file via a POST request to the `/upload` route.
- Verifies that the response status code is 200 and that the results contain the expected data.
- Cleans up by deleting the test PDF file.

## Detailed Code Explanation for GitHub Actions Workflow (`python-app.yml`)

The `python-app.yml` file is a GitHub Actions workflow configuration that automates the process of running tests and linting the code whenever changes are pushed to the repository.

### Workflow Triggers

The workflow is triggered on push and pull request events to the `main` branch.

### Permissions

Sets the permission to read contents of the repository.

### Jobs

#### `build` Job

- **Runs-on**: Specifies the job to run on the latest version of Ubuntu.
- **Steps**: Defines a series of steps to execute the job.

### Steps

1. **Checkout Repository**
    - Uses the `actions/checkout@v4` action to check out the repository's code.

2. **Set up Python**
    - Uses the `actions/setup-python@v3` action to set up Python 3.10.

3. **Uninstall fpdf2 if installed**
    - Runs a shell command to uninstall `fpdf2` if it is installed. This ensures there are no conflicts between `fpdf` and `fpdf2`.

4. **Install Dependencies**
    - Upgrades `pip` and installs the dependencies listed in `requirements.txt`.

5. **Lint with flake8**
    - Runs `flake8` to lint the code. It checks for Python syntax errors, undefined names, code complexity, and line length.

6. **Test with pytest**
    - Runs `pytest` to execute the test suite and ensure all tests pass.

### Notifications

- GitHub Actions sends notifications about the workflow status to users who have set up their notification preferences to receive such updates.

By following these steps, the workflow ensures that the code is linted and tested automatically, providing immediate feedback on the status of the codebase.

