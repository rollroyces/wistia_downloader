import requests
import re
import os

def extract_video_id(input_text):
    """Extract Wistia video ID from URL or page source."""
    patterns = [
        r'wvideo=([a-zA-Z0-9]+)',
        r'hashedId=([a-zA-Z0-9]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, input_text)
        if match:
            return match.group(1)
    return None

def get_video_url(video_id):
    """Fetch the embed page and extract the video URL."""
    embed_url = f"http://fast.wistia.net/embed/iframe/{video_id}"
    try:
        response = requests.get(embed_url)
        response.raise_for_status()
        page_source = response.text
        
        # Look for 'type: "original"' or 'type: "hd_mp4_video"'
        video_types = ['"type":"original"', '"type":"hd_mp4_video"']
        for video_type in video_types:
            type_index = page_source.find(video_type)
            if type_index != -1:
                # Find the URL in the next line
                url_start = page_source.find('"url":"', type_index)
                if url_start == -1:
                    continue
                url_end = page_source.find('"', url_start + 7)
                video_url = page_source[url_start + 7:url_end]
                if video_url.endswith('.bin'):
                    video_url = video_url.replace('.bin', '.mp4')
                return video_url
        return None
    except requests.RequestException as e:
        print(f"Error fetching embed page: {e}")
        return None

def download_video(video_url, output_filename):
    """Download the video from the given URL."""
    try:
        response = requests.get(video_url, stream=True)
        response.raise_for_status()
        with open(output_filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f"Video downloaded as {output_filename}")
    except requests.RequestException as e:
        print(f"Error downloading video: {e}")

def main():
    # Get input from user (URL or page source snippet)
    input_text = input("Enter the Wistia video URL or page source snippet: ")
    
    # Extract video ID
    video_id = extract_video_id(input_text)
    if not video_id:
        print("Could not find video ID in the provided input.")
        return
    
    print(f"Found video ID: {video_id}")
    
    # Get video URL
    video_url = get_video_url(video_id)
    if not video_url:
        print("Could not find video URL in the embed page.")
        return
    
    print(f"Found video URL: {video_url}")
    
    # Download the video
    output_filename = f"C://Downloads//wistia_video_{video_id}.mp4"
    download_video(video_url, output_filename)

if __name__ == "__main__":
    main()