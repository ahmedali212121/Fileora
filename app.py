 from flask import Flask, request, send_file, render_template_string
from pdf2docx import Converter
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>بلوري - PDF إلى Word</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f7fa;
            text-align: center;
            padding-top: 100px;
        }

        .box {
            background: white;
            width: 500px;
            max-width: 90%;
            margin: auto;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        }

        h1 {
            margin-bottom: 10px;
        }

        p {
            color: #666;
        }

        input {
            margin: 25px 0;
        }

        button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 14px 30px;
            border-radius: 10px;
            font-size: 16px;
            cursor: pointer;
        }

        button:hover {
            background: #1d4ed8;
        }
    </style>
</head>

<body>

<div class="box">
    <h1>بلوري 📄</h1>
    <h2>تحويل PDF إلى Word</h2>
    <p>اختر ملف PDF لتحويله إلى ملف Word</p>

    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="pdf_file" accept=".pdf" required>
        <br>
        <button type="submit">تحويل إلى Word</button>
    </form>
</div>

</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        file = request.files.get("pdf_file")

        if not file or file.filename == "":
            return "لم يتم اختيار ملف"

        if not file.filename.lower().endswith(".pdf"):
            return "يرجى اختيار ملف PDF فقط"

        file_id = str(uuid.uuid4())

        pdf_path = os.path.join(
            UPLOAD_FOLDER,
            file_id + ".pdf"
        )

        docx_path = os.path.join(
            OUTPUT_FOLDER,
            file_id + ".docx"
        )

        file.save(pdf_path)

        converter = Converter(pdf_path)
        converter.convert(docx_path)
        converter.close()

        return send_file(
            docx_path,
            as_attachment=True,
            download_name="بلوري-تحويل.docx"
        )

    return render_template_string(HTML)


if __name__ == "__main__":
    app.run(debug=True)
    