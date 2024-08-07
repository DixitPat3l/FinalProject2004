import os
import openai
import pdfplumber
import csv
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file (if it exists)
load_dotenv()

# Get the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("API key not found. Make sure you have set it in the environment or .env file.")

results = []

def chat_gpt(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response['choices'][0]['message']['content']

def pdf_to_text(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text
    return text

def suggest_best_job_fit(resume_text):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant specialized in recruitment and talent management."},
        {"role": "user", "content": f"Analyze this resume and provide only a list of top 3 job titles best suited for it: {resume_text} (i want only a list of top 3 job titles. No descriptions needed.)"}
    ]
    return chat_gpt(conversation)

def generate_sample_job_links(job_title):
    linkedin_link = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}"
    indeed_link = f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}"
    return linkedin_link, indeed_link

def update_csv(results):
    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Resume Name", "Comments", "Suitability", "Best Job Fit", "LinkedIn Job Link", "Indeed Job Link"])
        csv_writer.writerows(results)

@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    global results
    if request.method == 'POST':
        resume_files = request.files.getlist('file[]')
        job_description = request.form['job_description']
        mandatory_keywords = request.form['mandatory_keywords']

        if not resume_files or not job_description or not mandatory_keywords:
            return jsonify({"error": "Please provide resume files, a job description, and mandatory keywords."}), 400

        results = []
        for resume_file in resume_files:
            resume_text = pdf_to_text(resume_file)
            best_job_fit = suggest_best_job_fit(resume_text).strip()
            job_titles = best_job_fit.split('\n')
            linkedin_link, indeed_link = generate_sample_job_links(job_titles[0])

            conversation = [
                {"role": "system", "content": "You are a helpful assistant specialized in recruitment and talent management."},
                {"role": "user", "content": f"Mandatory keywords: {mandatory_keywords}"},
                {"role": "user", "content": f"Is this resume suitable for the job? Job description: {job_description}, Resume: {resume_text}  (also at the end of the prompt write if the candidate is Suitable, Not Suitable, or Maybe Suitable and the labels are mandatory to have)"}
            ]

            response = chat_gpt(conversation)

            # Replace newline characters with spaces in the response
            response = response.replace('\n', ' ')

            # Determine the suitability category
            response_lower = response.lower()
            if "not suitable" in response_lower:
                suitability = "Not Suitable"
            elif "maybe suitable" in response_lower:
                suitability = "Maybe Suitable"
            else:
                suitability = "Suitable"

            results.append([resume_file.filename, response, suitability, best_job_fit, linkedin_link, indeed_link])

        return jsonify({"results": results})
    else:  # Handling the GET request
        return render_template('upload.html')

@app.route('/download_csv', methods=['GET'])
def download_csv():
    global results
    update_csv(results)
    return send_file('results.csv', as_attachment=True)

@app.route('/')
def index():
    return render_template('upload.html')

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
