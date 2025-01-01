from flask import Flask, request, render_template, jsonify
import pandas as pd
import sweetviz as sv
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return "No file uploaded", 400

    # Read the uploaded file
    try:
        df = pd.read_csv(file)
    except Exception as e:
        return jsonify({"error": f"Failed to read file: {str(e)}"}), 400

    # Generate Sweetviz report
    report_path = "static/sweetviz_report.html"
    report = sv.analyze(df)
    report.show_html(filepath=report_path, open_browser=False)

    return jsonify({
        "message": "File uploaded and profiling report generated successfully.",
        "columns": list(df.columns),
        "rows": df.shape[0],
        "report_url": f"/{report_path}"
    })

if __name__ == '__main__':
    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
