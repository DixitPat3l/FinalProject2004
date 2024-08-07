import pytest
import os
from fpdf2 import FPDF
from flask import Flask
from werkzeug.datastructures import FileStorage
from screening_tool import app, pdf_to_text, suggest_best_job_fit, chat_gpt, generate_sample_job_links

# Configure the app for testing
app.config['TESTING'] = True

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def create_test_resume_pdf(path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    content = """John Doe
Data Analyst
Email: john.doe@example.com | Phone: (123) 456-7890 | LinkedIn: linkedin.com/in/johndoe

Summary:
Experienced Data Analyst with over 5 years of experience in data mining, data analysis, and statistical modeling. Proficient in Python, SQL, and data visualization tools like Tableau. Strong background in translating business requirements into actionable insights.

Professional Experience:

Data Analyst
XYZ Corporation, New York, NY
January 2019 – Present
- Conducted detailed data analysis using Python and SQL to identify trends and patterns in customer behavior.
- Developed and maintained dashboards in Tableau to visualize key performance metrics for stakeholders.
- Collaborated with cross-functional teams to define data requirements and provide data-driven insights for decision-making.

Junior Data Analyst
ABC Solutions, San Francisco, CA
June 2016 – December 2018
- Assisted in data collection and data cleaning processes for large datasets.
- Performed exploratory data analysis and created summary reports for various projects.
- Supported senior analysts in building predictive models using statistical techniques.

Education:

Bachelor of Science in Statistics
University of California, Berkeley
Graduated: May 2016

Skills:
- Data Analysis: Python, SQL, R
- Data Visualization: Tableau, Power BI, Matplotlib, Seaborn
- Statistical Modeling: Linear Regression, Logistic Regression, Time Series Analysis
- Database Management: MySQL, PostgreSQL

Projects:
- Customer Segmentation: Utilized clustering algorithms to segment customers based on purchasing behavior, resulting in targeted marketing campaigns that increased sales by 15%.
- Sales Forecasting: Developed a time series forecasting model to predict monthly sales, improving inventory management and reducing stockouts by 10%.

Certifications:
- Certified Data Scientist (CDS)
- Google Data Analytics Professional Certificate

Technical Proficiency:
- Programming Languages: Python, R, SQL
- Tools: Tableau, Power BI, Excel, Jupyter Notebook
- Databases: MySQL, PostgreSQL, MongoDB
"""
    pdf.multi_cell(0, 10, content)
    pdf.output(path)

def test_pdf_to_text():
    # Create a dummy PDF file for testing
    test_pdf_path = 'test_resume.pdf'
    create_test_resume_pdf(test_pdf_path)
    
    # Test the pdf_to_text function
    extracted_text = pdf_to_text(test_pdf_path)
    assert "John Doe" in extracted_text
    assert "Data Analyst" in extracted_text

    # Clean up
    os.remove(test_pdf_path)

def test_suggest_best_job_fit():
    resume_text = "Experienced software engineer with skills in Python, Flask, and API development."
    job_fit = suggest_best_job_fit(resume_text)
    assert "Software Engineer" in job_fit or "Python Developer" in job_fit

def test_generate_sample_job_links():
    job_title = "Software Engineer"
    linkedin_link, indeed_link = generate_sample_job_links(job_title)
    assert linkedin_link == f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}"
    assert indeed_link == f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}"

def test_chat_gpt():
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how can you assist me?"}
    ]
    response = chat_gpt(conversation)
    assert "assist" in response.lower()

def test_upload_resume(client):
    # Create a dummy PDF file for testing
    test_pdf_path = 'test_resume.pdf'
    create_test_resume_pdf(test_pdf_path)

    # Open the test PDF file
    with open(test_pdf_path, 'rb') as f:
        file = FileStorage(stream=f, filename='test_resume.pdf', content_type='application/pdf')

        data = {
            'file[]': file,
            'job_description': 'Software Engineer',
            'mandatory_keywords': 'Python, Flask'
        }
        response = client.post('/upload', data=data, content_type='multipart/form-data')
        json_data = response.get_json()

        assert response.status_code == 200
        assert 'results' in json_data

    # Clean up
    os.remove(test_pdf_path)