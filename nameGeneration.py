import re
from urllib.parse import urlparse, unquote, parse_qs

def sanitize_and_extract_title(video_url: str) -> tuple[str, str]:
    """
    Sanitizes a direct video download URL and extracts a usable title.
    
    Args:
        video_url (str): The input video URL.
    
    Returns:
        tuple[str, str]: (sanitized_url, title)
    """
    # Basic cleanup
    video_url = video_url.strip()

    # Validate URL
    parsed = urlparse(video_url)
    if not parsed.scheme.startswith("http") or not parsed.netloc:
        raise ValueError("Invalid URL: must start with http/https and include a domain.")

    # Remove tracking query parameters
    clean_query = {k: v for k, v in parse_qs(parsed.query).items() if not k.startswith("utm")}
    clean_query_str = "&".join(f"{k}={v[0]}" for k, v in clean_query.items()) if clean_query else ""

    # Reconstruct sanitized URL
    sanitized_url = parsed._replace(query=clean_query_str).geturl()

    # Extract filename or last path segment
    path = unquote(parsed.path)
    filename = path.split("/")[-1] or "video"
    
    # Try to remove file extension and clean the name
    title = re.sub(r'\.\w{2,5}$', '', filename)  # remove extension like .mp4
    title = re.sub(r'[-_]+', ' ', title)         # normalize separators
    title = re.sub(r'\s+', ' ', title).strip()   # trim and normalize whitespace

    # Fallback title if needed
    if not title:
        title = "video"

    return sanitized_url, title

