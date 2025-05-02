import requests
from bs4 import BeautifulSoup
import random
import time

# List of common User Agents
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; rv:118.0) Gecko/20100101 Firefox/118.0',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Mobile/15E148 Safari/604.1'
]
# Put here the base video listing menu URL
base_url = 'https://languagecourses.com/english/common-mistakes/page/'
video_links = set()

# Scrap of each page in the menu, modify the range according to your desired menu page total quantity of pages
for page_num in range(1, 9):
    url = f'{base_url}{page_num}/'
    headers = {'User-Agent': random.choice(user_agents)}  # User-Agent aleatorio
    print(f'Proccesingo: {url} con User-Agent: {headers["User-Agent"]}')
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f'Error at loading the page {url}: {e}')
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    for a in soup.find_all('a', href=True):
        href = a['href']
        # Put in here any common pattern you encounter in a video subpage (not the base_url which lists the videos)
        if '/english/common-mistakes/' in href and 'lesson' in href:
            # put here the main domain
            full_url = 'https://languagecourses.com' + href if href.startswith('/') else href
            video_links.add(full_url)

    # Random delay between 2 and 5 seconds
    delay = random.uniform(2, 5)
    print(f'Waiting {delay:.2f} seconds...\n')
    time.sleep(delay)

# Sort and save
video_links = sorted(video_links)
with open('video_urls.txt', 'w', encoding='utf-8') as f:
    for link in video_links:
        f.write(link + '\n')

# Print result
print(f'\nTotal number of pages found: {len(video_links)}\n')
for i, link in enumerate(video_links, start=1):
    print(f'{i}: {link}')
