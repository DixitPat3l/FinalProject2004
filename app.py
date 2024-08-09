import os
import openai
import pdfplumber
import csv
from io import StringIO
from flask import Flask, request, jsonify, render_template, send_file, send_from_directory, make_response
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
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        print(f"OpenAI API error: {str(e)}")
        return f"An error occurred: {str(e)}"


def pdf_to_text(file_path):
    text = ''
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
    except Exception as e:
        print(f"Error reading PDF file: {str(e)}")
    return text


def suggest_best_job_fit(resume_text):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant specialized in recruitment and talent management."},
        {"role": "user",
         "content": f"Analyze this resume and provide only a list of top 3 job titles best suited for it: {resume_text} (I want only a list of top 3 job titles. No descriptions needed.)"}
    ]
    return chat_gpt(conversation)


def evaluate_resume(resume_text, job_description, mandatory_keywords):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant specialized in recruitment and talent management."},
        {"role": "user", "content": (
            f"Is this resume suitable for the job? Job description: {job_description}, Resume: {resume_text}. "
            f"Provide a very brief evaluation in one sentence, without using bullet points. "
            f"End with the final decision as 'Suitable', 'Not Suitable', or 'Maybe Suitable'."
        )}
    ]
    return chat_gpt(conversation)


def generate_sample_job_links(job_title):
    linkedin_link = f"https://www.linkedin.com/jobs/search/?keywords={job_title.replace(' ', '%20')}"
    indeed_link = f"https://www.indeed.com/jobs?q={job_title.replace(' ', '+')}"
    return linkedin_link, indeed_link


def extract_keywords(job_description):
    conversation = [
        {"role": "system", "content": "You are a helpful assistant specialized in recruitment and talent management."},
        {"role": "user", "content": (
            f"Extract the 5 most relevant keywords from the following job description. "
            "List only the keywords, separated by commas. Do not include any extra text, such as 'Keywords:' or numbers."
        )},
        {"role": "user", "content": job_description}
    ]
    response = chat_gpt(conversation)
    # Split the response into individual keywords, ensuring no extra formatting
    keywords = response.split(',')
    return [keyword.strip() for keyword in keywords[:5]]

@app.route('/generate_keywords', methods=['POST'])
def generate_keywords():
    data = request.json
    job_description = data.get('job_description', '')

    if not job_description:
        return jsonify({"error": "Job description is required."}), 400

    keywords = extract_keywords(job_description)
    return jsonify({"keywords": keywords})


@app.route('/upload', methods=['GET', 'POST'])
def upload_resume():
    global results
    if request.method == 'POST':
        try:
            resume_files = request.files.getlist('file[]')
            job_description = request.form['job_description']
            mandatory_keywords = request.form['mandatory_keywords']

            if not resume_files or not job_description or not mandatory_keywords:
                return jsonify(
                    {"error": "Please provide resume files, a job description, and mandatory keywords."}), 400

            results = []
            for resume_file in resume_files:
                filename = secure_filename(resume_file.filename)
                resume_text = pdf_to_text(resume_file)

                if not resume_text:
                    return jsonify({"error": f"Could not extract text from {filename}."}), 500

                best_job_fit = suggest_best_job_fit(resume_text).strip()
                job_titles = best_job_fit.split('\n')
                linkedin_link, indeed_link = generate_sample_job_links(job_titles[0])

                response = evaluate_resume(resume_text, job_description, mandatory_keywords)

                if "An error occurred" in response:
                    return jsonify({"error": f"OpenAI API failed for {filename}: {response}"}), 500

                suitability = "Unknown"
                if "Not Suitable" in response:
                    suitability = "Not Suitable"
                elif "Maybe Suitable" in response:
                    suitability = "Maybe Suitable"
                elif "Suitable" in response:
                    suitability = "Suitable"

                results.append([filename, response, suitability, best_job_fit, linkedin_link, indeed_link])

            return jsonify({"results": results})
        except Exception as e:
            print(f"Error during resume processing: {str(e)}")
            return jsonify({"error": "An internal error occurred during resume processing."}), 500
    else:  # Handling the GET request
        return render_template('upload.html')


@app.route('/download_csv', methods=['GET'])
def download_csv():
    try:
        if not results:
            return jsonify({"error": "No results available to download."}), 400

        # Generate the CSV in memory
        output = StringIO()
        csv_writer = csv.writer(output)
        csv_writer.writerow(["Resume Name", "Comments", "Suitability", "Best Job Fit", "LinkedIn Job Link", "Indeed Job Link"])
        csv_writer.writerows(results)
        output.seek(0)

        # Create a response with the CSV content
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=results.csv"
        response.headers["Content-type"] = "text/csv"
        return response

    except Exception as e:
        print(f"Error sending CSV file: {str(e)}")
        return jsonify({"error": "An error occurred while generating the CSV file."}), 500

def update_csv(results):
    try:
        with open('results.csv', 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Resume Name", "Comments", "Suitability", "Best Job Fit", "LinkedIn Job Link", "Indeed Job Link"])
            csv_writer.writerows(results)
    except Exception as e:
        print(f"Error writing to CSV: {str(e)}")



@app.route('/')
def index():
    return render_template('upload.html')


if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=True)
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")
