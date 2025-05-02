# getMetadata.py

import re
import nameGeneration  # Import the name generation module

video_urls_file = 'video_urls.txt'
real_video_urls_file = 'real_video_urls.txt'
output_file = 'video_metadata.txt'

# You can easily replace this line with other custom name generation functions
def url_to_filename(url):
    # You can call any function you import here;
    return nameGeneration.sanitize_and_extract_title(url)

# Reading URLs from both input files
with open(video_urls_file, 'r', encoding='utf-8') as f:
    video_urls = [line.strip() for line in f if line.strip()]

with open(real_video_urls_file, 'r', encoding='utf-8') as f:
    real_video_urls = [line.strip() for line in f if line.strip()]

# Ensure both files have the same number of URLs
if len(video_urls) != len(real_video_urls):
    print("Error: The number of URLs in 'video_urls.txt' and 'real_video_urls.txt' don't match.")
    exit(1)

# Writing metadata to the output file
with open(output_file, 'w', encoding='utf-8') as f:
    for video_url, real_url in zip(video_urls, real_video_urls):
        smart_title = url_to_filename(video_url)
        f.write(f'URL: {real_url} TITLE: {smart_title}\n')

print(f'✓ Finished generating {len(video_urls)} metadata entries.')
print(f'✓ Saved as: {output_file}')
