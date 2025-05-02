import os
import requests
import time
import random
import re
from tqdm import tqdm  # Import tqdm for progress bar

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1'
]

input_file = 'video_metadata.txt'
output_dir = 'videos'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Function to sanitize the filename
def sanitize_filename(filename):
    # Remove any invalid characters (Windows specific)
    return re.sub(r'[<>:"/\\|?*]', '', filename)

# Load video metadata
with open(input_file, 'r', encoding='utf-8') as file:
    metadata = [line.strip() for line in file if line.strip()]

# Download each video and save with the sanitized TITLE
for i, entry in enumerate(metadata, start=1):
    # Split URL and TITLE from the entry
    parts = entry.split('TITLE: ')
    if len(parts) == 2:
        url, title = parts
        url = url.replace('URL: ', '').strip()  # Clean up the URL
        title = sanitize_filename(title.strip())  # Clean up the title for filename

        # Construct the filepath with the sanitized title
        filename = f"{title}.mp4"
        filepath = os.path.join(output_dir, filename)

        headers = {'User-Agent': random.choice(user_agents)}

        print(f"[{i}/{len(metadata)}] Downloading: {url} → {filename}")

        try:
            # Start the request and get the file size for progress bar
            with requests.get(url, headers=headers, stream=True, timeout=60) as r:
                r.raise_for_status()

                total_size = int(r.headers.get('content-length', 0))  # Get total size of the file
                with open(filepath, 'wb') as f:
                    # Use tqdm for the progress bar
                    with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as pbar:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))  # Update the progress bar with the chunk size
            print(f"→ Saved: {filepath}")
        except requests.RequestException as e:
            print(f"✖ Failed to download {url}: {e}")

        time.sleep(random.uniform(2, 5))  # Delay between downloads

print(f"\n✓ Done. Videos saved in the '{output_dir}' folder with the respective titles.")
