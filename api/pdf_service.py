import weasyprint


def html_to_pdf(html_string: str) -> bytes:
    """Convert an HTML string to PDF bytes using WeasyPrint."""
    return weasyprint.HTML(string=html_string).write_pdf()
