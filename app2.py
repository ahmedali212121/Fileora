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


# =========================================================
# Ø§Ù„ØµÙØ­Ø© Ø§Ù„Ø±Ø¦ÙŠØ³ÙŠØ©
# =========================================================

@app.route("/")
def home():
    return render_template("home.html")


# =========================================================
# robots.txt
# =========================================================

@app.route("/robots.txt")
def robots_txt():
    content = """User-agent: *
Allow: /

Sitemap: https://nextoolia.com/sitemap.xml
"""
    return Response(content, mimetype="text/plain")


# =========================================================
# ads.txt
# =========================================================

@app.route("/ads.txt")
def ads_txt():
    content = """google.com, pub-5168430877675005, DIRECT, f08c47fec0942fa0
"""
    return Response(content, mimetype="text/plain")


# =========================================================
# sitemap.xml
# =========================================================

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


# =========================================================
# Ø³ÙŠØ§Ø³Ø© Ø§Ù„Ø®ØµÙˆØµÙŠØ©
# =========================================================

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


# =========================================================
# Ø´Ø±ÙˆØ· Ø§Ù„Ø§Ø³ØªØ®Ø¯Ø§Ù…
# =========================================================

@app.route("/terms")
def terms():
    return render_template("terms.html")


# =========================================================
# Ù…Ù† Ù†Ø­Ù†
# =========================================================

@app.route("/about")
def about():
    return render_template("about.html")


# =========================================================
# Ø§ØªØµÙ„ Ø¨Ù†Ø§
# =========================================================

@app.route("/contact")
def contact():
    return render_template("contact.html")


# =========================================================
# PDF Ø¥Ù„Ù‰ Word
# =========================================================

@app.route("/pdf-to-word", methods=["GET", "POST"])
def pdf_to_word():

    if request.method == "POST":

        file = request.files.get("pdf_file")

        if not file or file.filename == "":
            return "Ù„Ù… ÙŠØªÙ… Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù PDF"

        if not file.filename.lower().endswith(".pdf"):
            return "ÙŠØ±Ø¬Ù‰ Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù PDF ÙÙ‚Ø·"

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
            <h2>Ø­Ø¯Ø« Ø®Ø·Ø£</h2>
            <p>{e}</p>
            <a href="/pdf-to-word">Ø§Ù„Ø¹ÙˆØ¯Ø©</a>
            """

    return render_template("pdf_to_word.html")


# =========================================================
# Word Ø¥Ù„Ù‰ PDF
# =========================================================

@app.route("/word-to-pdf", methods=["GET", "POST"])
def word_to_pdf():

    if request.method == "POST":

        file = request.files.get("word_file")

        if not file or file.filename == "":
            return "Ù„Ù… ÙŠØªÙ… Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù Word"

        filename = file.filename.lower()

        if not (
            filename.endswith(".docx")
            or filename.endswith(".doc")
        ):
            return "ÙŠØ±Ø¬Ù‰ Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù Word ÙÙ‚Ø·"

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
            <h2>Ø­Ø¯Ø« Ø®Ø·Ø£ Ø£Ø«Ù†Ø§Ø¡ Ø§Ù„ØªØ­ÙˆÙŠÙ„</h2>
            <p>{e}</p>
            <a href="/word-to-pdf">Ø§Ù„Ø¹ÙˆØ¯Ø©</a>
            """

    return render_template("word_to_pdf.html")


# =========================================================
# Ø¯Ù…Ø¬ PDF
# =========================================================

@app.route("/merge-pdf", methods=["GET", "POST"])
def merge_pdf():

    if request.method == "POST":

        files = request.files.getlist("pdf_files")

        files = [
            file
            for file in files
            if file and file.filename != ""
        ]

        if len(files) < 2:
            return "Ø§Ø®ØªØ± Ù…Ù„ÙÙŠÙ† PDF Ø¹Ù„Ù‰ Ø§Ù„Ø£Ù‚Ù„"

        file_id = str(uuid.uuid4())

        pdf_files = []

        try:

            for index, file in enumerate(files):

                if not file.filename.lower().endswith(".pdf"):
                    return "Ø¬Ù…ÙŠØ¹ Ø§Ù„Ù…Ù„ÙØ§Øª ÙŠØ¬Ø¨ Ø£Ù† ØªÙƒÙˆÙ† PDF"

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

            writer.close()

            return send_file(
                output_path,
                as_attachment=True,
                download_name="NexToolia-Merged.pdf"
            )

        except Exception as e:

            return f"""
            <h2>Ø­Ø¯Ø« Ø®Ø·Ø£ Ø£Ø«Ù†Ø§Ø¡ Ø§Ù„Ø¯Ù…Ø¬</h2>
            <p>{e}</p>
            <a href="/merge-pdf">Ø§Ù„Ø¹ÙˆØ¯Ø©</a>
            """

    return render_template("merge_pdf.html")


# =========================================================
# Ø¶ØºØ· PDF
# =========================================================

@app.route("/compress-pdf", methods=["GET", "POST"])
def compress_pdf():

    if request.method == "POST":

        file = request.files.get("pdf_file")

        if not file or file.filename == "":
            return "Ù„Ù… ÙŠØªÙ… Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù PDF"

        if not file.filename.lower().endswith(".pdf"):
            return "ÙŠØ±Ø¬Ù‰ Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù PDF"

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

            writer.add_metadata({})

            with open(output_path, "wb") as output_file:
                writer.write(output_file)

            return send_file(
                output_path,
                as_attachment=True,
                download_name="NexToolia-Compressed.pdf"
            )

        except Exception as e:

            return f"""
            <h2>Ø­Ø¯Ø« Ø®Ø·Ø£ Ø£Ø«Ù†Ø§Ø¡ Ø§Ù„Ø¶ØºØ·</h2>
            <p>{e}</p>
            <a href="/compress-pdf">Ø§Ù„Ø¹ÙˆØ¯Ø©</a>
            """

    return render_template("compress_pdf.html")


# =========================================================
# ØªÙ‚Ø³ÙŠÙ… PDF
# =========================================================

@app.route("/split-pdf", methods=["GET", "POST"])
def split_pdf():

    if request.method == "POST":

        file = request.files.get("pdf_file")

        start_page = request.form.get("start_page")
        end_page = request.form.get("end_page")

        if not file or file.filename == "":
            return "Ù„Ù… ÙŠØªÙ… Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù PDF"

        if not file.filename.lower().endswith(".pdf"):
            return "ÙŠØ±Ø¬Ù‰ Ø§Ø®ØªÙŠØ§Ø± Ù…Ù„Ù PDF ÙÙ‚Ø·"

        try:

            start_page = int(start_page)
            end_page = int(end_page)

        except (TypeError, ValueError):

            return "Ø£Ø¯Ø®Ù„ Ø£Ø±Ù‚Ø§Ù… ØµÙØ­Ø§Øª ØµØ­ÙŠØ­Ø©"

        if start_page < 1 or end_page < start_page:
            return "Ù†Ø·Ø§Ù‚ Ø§Ù„ØµÙØ­Ø§Øª ØºÙŠØ± ØµØ­ÙŠØ­"

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
                return (
                    f"Ø§Ù„Ù…Ù„Ù ÙŠØ­ØªÙˆÙŠ Ø¹Ù„Ù‰ "
                    f"{total_pages} ØµÙØ­Ø§Øª ÙÙ‚Ø·"
                )

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
            <h2>Ø­Ø¯Ø« Ø®Ø·Ø£ Ø£Ø«Ù†Ø§Ø¡ ØªÙ‚Ø³ÙŠÙ… PDF</h2>
            <p>{e}</p>
            <a href="/split-pdf">Ø§Ù„Ø¹ÙˆØ¯Ø©</a>
            """

    return render_template("split_pdf.html")


# =========================================================
# ØªØ´ØºÙŠÙ„ Ø§Ù„ØªØ·Ø¨ÙŠÙ‚
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )


