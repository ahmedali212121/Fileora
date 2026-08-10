from flask import Flask, request, send_file, render_template, Response
from pdf2docx import Converter
from docx2pdf import convert
from pypdf import PdfWriter, PdfReader
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/robots.txt")
def robots_txt():
    content = """User-agent: *
Allow: /
Sitemap: https://nextoolia.com/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


@app.route("/ads.txt")
def ads_txt():
    content = """google.com, pub-5168430877675005, DIRECT, f08c47fec0942fa0
"""
    return Response(content, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">

    <url>
        <loc>https://nextoolia.com/</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/pdf-to-word</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/word-to-pdf</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/merge-pdf</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/compress-pdf</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/split-pdf</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/privacy</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/terms</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/about</loc>
    </url>

    <url>
        <loc>https://nextoolia.com/contact</loc>
    </url>

</urlset>
"""
    return Response(content, mimetype="application/xml")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/pdf-to-word", methods=["GET", "POST"])
def pdf_to_word():
    if request.method == "POST":
        file = request.files.get("pdf_file")

        if not file or file.filename == "":
            return "لم يتم اختيار ملف PDF"

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

        try:
            converter = Converter(pdf_path)
            converter.convert(docx_path)
            converter.close()

            return send_file(
                docx_path,
                as_attachment=True,
                download_name="NexToolia.docx"
            )

        except Exception as e:
            return f"""
            <h2>حدث خطأ</h2>
            <p>{e}</p>
            <a href="/pdf-to-word">العودة</a>
            """

    return render_template("pdf_to_word.html")


@app.route("/word-to-pdf", methods=["GET", "POST"])
def word_to_pdf():
    if request.method == "POST":
        file = request.files.get("word_file")

        if not file or file.filename == "":
            return "لم يتم اختيار ملف Word"

        filename = file.filename.lower()

        if not (
            filename.endswith(".docx")
            or filename.endswith(".doc")
        ):
            return "يرجى اختيار ملف Word فقط"

        file_id = str(uuid.uuid4())

        extension = (
            ".docx"
            if filename.endswith(".docx")
            else ".doc"
        )

        word_path = os.path.join(
            UPLOAD_FOLDER,
            file_id + extension
        )

        pdf_path = os.path.join(
            OUTPUT_FOLDER,
            file_id + ".pdf"
        )

        file.save(word_path)

        try:
            convert(word_path, pdf_path)

            return send_file(
                pdf_path,
                as_attachment=True,
                download_name="NexToolia.pdf"
            )

        except Exception as e:
            return f"""
            <h2>حدث خطأ أثناء التحويل</h2>
            <p>{e}</p>
            <a href="/word-to-pdf">العودة</a>
            """

    return render_template("word_to_pdf.html")


@app.route("/merge-pdf", methods=["GET", "POST"])
def merge_pdf():
    if request.method == "POST":
        files = [
            file
            for file in request.files.getlist("pdf_files")
            if file and file.filename != ""
        ]

        if len(files) < 2:
            return "اختر ملفين PDF على الأقل"

        file_id = str(uuid.uuid4())
        pdf_files = []

        try:
            for index, file in enumerate(files):
                if not file.filename.lower().endswith(".pdf"):
                    return "جميع الملفات يجب أن تكون PDF"

                path = os.path.join(
                    UPLOAD_FOLDER,
                    f"{file_id}_{index}.pdf"
                )

                file.save(path)
                pdf_files.append(path)

            output_path = os.path.join(
                OUTPUT_FOLDER,
                file_id + "_merged.pdf"
            )

            writer = PdfWriter()

            for pdf_path in pdf_files:
                reader = PdfReader(pdf_path)

                for page in reader.pages:
                    writer.add_page(page)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            return send_file(
                output_path,
                as_attachment=True,
                download_name="NexToolia-Merged.pdf"
            )

        except Exception as e:
            return f"""
            <h2>حدث خطأ أثناء الدمج</h2>
            <p>{e}</p>
            <a href="/merge-pdf">العودة</a>
            """

    return render_template("merge_pdf.html")


@app.route("/compress-pdf", methods=["GET", "POST"])
def compress_pdf():
    if request.method == "POST":
        file = request.files.get("pdf_file")

        if not file or file.filename == "":
            return "لم يتم اختيار ملف PDF"

        if not file.filename.lower().endswith(".pdf"):
            return "يرجى اختيار ملف PDF"

        file_id = str(uuid.uuid4())

        input_path = os.path.join(
            UPLOAD_FOLDER,
            file_id + "_original.pdf"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            file_id + "_compressed.pdf"
        )

        file.save(input_path)

        try:
            reader = PdfReader(input_path)
            writer = PdfWriter()

            for page in reader.pages:
                try:
                    page.compress_content_streams()
                except Exception:
                    pass

                writer.add_page(page)

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            return send_file(
                output_path,
                as_attachment=True,
                download_name="NexToolia-Compressed.pdf"
            )

        except Exception as e:
            return f"""
            <h2>حدث خطأ أثناء الضغط</h2>
            <p>{e}</p>
            <a href="/compress-pdf">العودة</a>
            """

    return render_template("compress_pdf.html")


@app.route("/split-pdf", methods=["GET", "POST"])
def split_pdf():
    if request.method == "POST":
        file = request.files.get("pdf_file")

        start_page = request.form.get("start_page")
        end_page = request.form.get("end_page")

        if not file or file.filename == "":
            return "لم يتم اختيار ملف PDF"

        if not file.filename.lower().endswith(".pdf"):
            return "يرجى اختيار ملف PDF فقط"

        try:
            start_page = int(start_page)
            end_page = int(end_page)

        except (TypeError, ValueError):
            return "أدخل أرقام صفحات صحيحة"

        if start_page < 1 or end_page < start_page:
            return "نطاق الصفحات غير صحيح"

        file_id = str(uuid.uuid4())

        input_path = os.path.join(
            UPLOAD_FOLDER,
            file_id + ".pdf"
        )

        file.save(input_path)

        try:
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)

            if end_page > total_pages:
                return f"الملف يحتوي على {total_pages} صفحات فقط"

            output_path = os.path.join(
                OUTPUT_FOLDER,
                file_id + "_split.pdf"
            )

            writer = PdfWriter()

            for page_number in range(
                start_page - 1,
                end_page
            ):
                writer.add_page(
                    reader.pages[page_number]
                )

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            return send_file(
                output_path,
                as_attachment=True,
                download_name="NexToolia-Split.pdf"
            )

        except Exception as e:
            return f"""
            <h2>حدث خطأ أثناء تقسيم PDF</h2>
            <p>{e}</p>
            <a href="/split-pdf">العودة</a>
            """

    return render_template("split_pdf.html")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )