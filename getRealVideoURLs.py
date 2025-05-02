import requests
from bs4 import BeautifulSoup
import random
import time

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1'
]

input_file = 'video_urls.txt'
output_file = 'real_video_urls.txt'
video_sources = []

with open(input_file, 'r', encoding='utf-8') as file:
    urls = [line.strip() for line in file if line.strip()]

for i, url in enumerate(urls, start=1):
    headers = {'User-Agent': random.choice(user_agents)}
    print(f'[{i}/{len(urls)}] Processing: {url}')
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'Error in {url}: {e}')
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # Search <video> tag and it's respective <source>
    video_tag = soup.find('video')
    if video_tag:
        source_tag = video_tag.find('source', attrs={'type': 'video/mp4'})
        if source_tag and source_tag.get('src'):
            video_src = source_tag['src']
            if not video_src.startswith('http'):
                # put here the direct video url base common pattern
                video_src = 'https://languagecourses.com' + video_src  # adjusts if the src is relative
            video_sources.append(video_src)
            print(f'→ Encontrado: {video_src}')
        else:
            print('✖ <source type="video/mp4"> was not found in the <video> tag.')
    else:
        print('✖ <video> tag was not found.')

    #time.sleep(random.uniform(2, 4))  # Random delay to not overload the server

# Guardar URLs en archivo
with open(output_file, 'w', encoding='utf-8') as f:
    for src in video_sources:
        f.write(src + '\n')

print(f'\n✓ Total extracted URL: {len(video_sources)}')
print(f'✓ Saved as: {output_file}')