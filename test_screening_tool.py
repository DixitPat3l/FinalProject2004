import pytest
import os
from fpdf import FPDF
from werkzeug.datastructures import FileStorage
from app import app, pdf_to_text, suggest_best_job_fit, chat_gpt, generate_sample_job_links, update_csv

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
    content = """
    John Doe
    Data Analyst
    Email: john.doe@example.com | Phone: (123) 456-7890 | LinkedIn: linkedin.com/in/johndoe

    Summary:
    Experienced Data Analyst with over 5 years of experience in data mining, data analysis, and statistical modeling. Proficient in Python, SQL, and data visualization tools like Tableau. Strong background in translating business requirements into actionable insights.

    Professional Experience:

    1. Data Analyst
    XYZ Corporation, New York, NY
    January 2019 to Present
    Conducted detailed data analysis using Python and SQL to identify trends and patterns in customer behavior.
    Developed and maintained dashboards in Tableau to visualize key performance metrics for stakeholders.
    Collaborated with cross-functional teams to define data requirements and provide data-driven insights for decision-making.

    2. Junior Data Analyst
    ABC Solutions, San Francisco, CA
    June 2016 to December 2018
    Assisted in data collection and data cleaning processes for large datasets.
    Performed exploratory data analysis and created summary reports for various projects.
    Supported senior analysts in building predictive models using statistical techniques.

    Education:

    Bachelor of Science in Statistics
    University of California, Berkeley
    Graduated: May 2016

    Skills:
    Data Analysis: Python, SQL, R
    Data Visualization: Tableau, Power BI, Matplotlib, Seaborn
    Statistical Modeling: Linear Regression, Logistic Regression, Time Series Analysis
    Database Management: MySQL, PostgreSQL

    Projects:
    1. Customer Segmentation: Utilized clustering algorithms to segment customers based on purchasing behavior, resulting in targeted marketing campaigns that increased sales by 15%.
    2. Sales Forecasting: Developed a time series forecasting model to predict monthly sales, improving inventory management and reducing stockouts by 10%.

    Certifications:
    Certified Data Scientist (CDS)
    Google Data Analytics Professional Certificate

    Technical Proficiency:
    Programming Languages: Python, R, SQL
    Tools: Tableau, Power BI, Excel, Jupyter Notebook
    Databases: MySQL, PostgreSQL, MongoDB
    """
    pdf.multi_cell(0, 10, content)
    pdf.output(path, 'F')


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
    assert any(keyword in job_fit for keyword in
               ["Software Engineer", "Python Developer", "Software Developer", "API Development Engineer",
                "Flask Web Developer"])


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


def test_download_csv(client):
    # Create a simple CSV content for testing in memory
    test_results = [
        ["Test Resume", "Test comment", "Suitable", "Software Engineer", "https://linkedin.com", "https://indeed.com"]
    ]

    # Update CSV in memory
    output = io.StringIO()
    csv_writer = csv.writer(output)
    csv_writer.writerow(["Resume Name", "Comments", "Suitability", "Best Job Fit", "LinkedIn Job Link", "Indeed Job Link"])
    csv_writer.writerows(test_results)
    output.seek(0)

    # Mock the update_csv function to return the in-memory CSV
    with patch('app.update_csv', return_value=output.getvalue()):
        # Test the download_csv route
        response = client.get('/download_csv')

        # Check if the file is returned
        assert response.status_code == 200
        assert 'text/csv' in response.content_type
        assert 'attachment' in response.headers['Content-Disposition']

        # Check if the CSV content is correct
        assert b"Test Resume" in response.data
        assert b"Software Engineer" in response.data
