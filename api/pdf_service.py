import pdfkit


def html_to_pdf(html_string: str) -> bytes:
    """Convert an HTML string to PDF bytes using wkhtmltopdf."""
    return pdfkit.from_string(html_string, False)
