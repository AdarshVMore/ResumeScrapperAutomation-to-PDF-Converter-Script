import subprocess
import os
import sys

WKHTMLTOPDF_PATH = "/usr/local/bin/wkhtmltopdf"

HTML_FILE = "resume.html"
PDF_FILE = "resume.pdf"

def generate_pdf():
    if not os.path.exists(HTML_FILE):
        print(f"❌ HTML file not found: {HTML_FILE}")
        sys.exit(1)

    command = [
        WKHTMLTOPDF_PATH,
        "--enable-local-file-access",   # CRITICAL for local CSS/assets
        "--print-media-type",
        "--margin-top", "10mm",
        "--margin-bottom", "10mm",
        "--margin-left", "10mm",
        "--margin-right", "10mm",
        HTML_FILE,
        PDF_FILE
    ]

    try:
        subprocess.run(command, check=True)
        print(f"✅ PDF generated successfully: {PDF_FILE}")

    except subprocess.CalledProcessError as e:
        print("❌ PDF generation failed")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    generate_pdf()