import os


SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]
SUPABASE_BUCKET = os.environ.get("SUPABASE_BUCKET", "pdfs")

MAX_HTML_SIZE = 5 * 1024 * 1024  # 5MB
