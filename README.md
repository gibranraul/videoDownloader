# 📥 VideoDownloader

**VideoDownloader** is a Python script that scrapes video subpages from a course listing page, extracts direct `.mp4` URLs by parsing each HTML page, and downloads all videos in bulk. It's designed for structured educational websites with static HTML pages.

## Features

- Extracts video subpage links from a main listing page  
- Parses each subpage to locate the actual video download URL  
- Compiles all video URLs and downloads them automatically

## Example

From a listing page base url like:

```
https://languagecourses.com/english/common-mistakes/page/
```

It finds subpages such as:

```
https://languagecourses.com/english/common-mistakes/lesson-1-16072012-0916
```

Then extracts the direct video link:

```
https://languagecourses.com/english/common-mistakes/16072012-0916.mp4
```

## Usage

1. Clone the repo
2. Install required libraries:
   ```bash
   pip install -r requirements.txt
   ```
3. Edit the 'getVideoPages' base_url variable to the video listing webpage you wanna scrap the video pages urls from, follow the comment instructions in that file
4. Run 'getVideoPages' script and you'll get a video_urls.txt file with all the video pages urls
5. Run getRealVideoURLs to scrap the direct video urls by scraping each url from the video_urls.txt and you'll get a real_video_urls.txt file
6. Run 'getMetadata' to generate a metadata file with all the direct video urls and titles for each video
7. Run downloadVIdeoFiles to start downloading all the files and save them into a 'videos' folder with the generated titles in the metadata file.

## Notes

- Make sure the site structure follows a consistent HTML pattern  
- Use responsibly and respect the site's terms of use

---

Feel free to contribute or report issues!
