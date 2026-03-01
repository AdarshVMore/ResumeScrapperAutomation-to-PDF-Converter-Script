import time
from supabase import create_client

from api.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET

_client = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_pdf(pdf_bytes: bytes, filename: str) -> str:
    """Upload PDF bytes to Supabase Storage and return the public URL."""
    # Prefix with timestamp to avoid filename collisions
    storage_path = f"{int(time.time())}_{filename}"

    _client.storage.from_(SUPABASE_BUCKET).upload(
        path=storage_path,
        file=pdf_bytes,
        file_options={"content-type": "application/pdf"},
    )

    public_url = _client.storage.from_(SUPABASE_BUCKET).get_public_url(storage_path)
    return public_url
