import os
import openai
import pdfplumber
import csv
from flask import Flask, request, jsonify, render_template, send_file
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("API key not found. Make sure you have set it in the .env file.")

results = []

def chat_gpt(conversation):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation
    )
    return response.choices[0].message['content']

def pdf_to_text(file_path):
    text = ''
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text()
    return text

def update_csv(results):
    with open('results.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Resume Name", "Comments", "Suitability"])
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

            results.append([resume_file.filename, response, suitability])

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
