import os
import re

def clean_filename(s):
    # Keep only safe characters (avoid invalid file characters for Windows)
    return re.sub(r'[^a-zA-Z0-9\-_. ]', '_', s)

# Load metadata (URL and TITLE)
metadata_file = 'video_metadata.txt'
metadata = []

with open(metadata_file, 'r', encoding='utf-8') as f:
    for line in f:
        if line.strip():
            title_part = line.strip().split('TITLE: ')[1]
            metadata.append(title_part.strip())

# Get list of .mp4 files
video_folder = 'videos'
video_files = sorted([f for f in os.listdir(video_folder) if f.endswith('.mp4')])

# Check consistency between the number of video files and metadata entries
if len(video_files) != len(metadata):
    print("⚠️ Warning: Number of video files and metadata entries doesn't match!")
    print(f"Files: {len(video_files)} | Metadata Entries: {len(metadata)}")
    raise ValueError("Mismatch between video files and metadata entries! Aborting...")

# If the check passes, proceed with renaming
for i, file in enumerate(video_files):
    old_filename = os.path.join(video_folder, file)
    new_title = metadata[i]
    safe_name = clean_filename(new_title)  # Sanitize the filename

    new_filename = os.path.join(video_folder, f"{safe_name}.mp4")

    if not os.path.exists(new_filename):
        os.rename(old_filename, new_filename)
        print(f"✓ Renamed: {file} → {safe_name}.mp4")
    else:
        print(f"✗ Skipped (already exists): {safe_name}.mp4")
