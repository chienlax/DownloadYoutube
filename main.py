import subprocess

def run_extract_links():
    """Runs extract_link.py to extract video links from a playlist."""
    try:
        print("Running extract_link.py to get video links...")
        playlist_url = input("Enter YouTube Playlist URL: ") # Get playlist URL here
        subprocess.run(["python", "extract_link.py", playlist_url], check=True) # Execute extract_link.py, pass URL as argument
        print("Video link extraction complete. Links saved to video_links.txt")
    except subprocess.CalledProcessError as e:
        print(f"Error running extract_link.py: {e}")
    except FileNotFoundError:
        print("Error: extract_link.py not found. Make sure it's in the same directory.")

def run_single_video_downloader():
    """Runs video_downloader_mp3.py to download a single video."""
    try:
        print("\nRunning video_downloader_mp3.py for single video download...")
        video_url = input("Enter YouTube Video URL: ") # Get single video URL here
        download_directory = input("Enter download directory (leave blank for current directory): ") or "."
        subprocess.run(["python", "video_downloader_mp3.py", video_url, download_directory], check=True) # Execute video_downloader_mp3.py, pass URL and directory as arguments
        print("Single video MP3 download process complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error running video_downloader_mp3.py: {e}")
    except FileNotFoundError:
        print("Error: video_downloader_mp3.py not found. Make sure it's in the same directory.")

def run_playlist_video_downloader():
    """Runs video_downloader_mp3.py to download MP3s from video links in video_links.txt."""
    try:
        print("\nRunning video_downloader_mp3.py for playlist download...")
        download_directory = input("Enter download directory (leave blank for current directory): ") or "."
        subprocess.run(["python", "video_downloader_mp3.py", "--playlist", download_directory], check=True) # Execute video_downloader_mp3.py with --playlist flag and directory
        print("Playlist MP3 download process complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error running video_downloader_mp3.py: {e}")
    except FileNotFoundError:
        print("Error: video_downloader_mp3.py not found. Make sure it's in the same directory.")

def run_webm_to_mp4_converter():
    """Runs webm_to_mp4_converter.py to convert WEBM files to MP4."""
    try:
        print("\nRunning webm_to_mp4_converter.py to convert WEBM files to MP4...")
        subprocess.run(["python", "webm_to_mp4_converter.py"], check=True) # Execute webm_to_mp4_converter.py
        print("WEBM to MP4 conversion complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error running webm_to_mp4_converter.py: {e}")
    except FileNotFoundError:
        print("Error: webm_to_mp4_converter.py not found. Make sure it's in the same directory.")

def run_mp3_metadata_editor():
    """Runs mp3_metadata_editor.py to edit MP3 and MP4 metadata."""
    try:
        print("\nRunning mp3_metadata_editor.py to edit metadata...")
        subprocess.run(["python", "mp3_metadata_editor.py"], check=True) # Execute mp3_metadata_editor.py
        print("Metadata editing process complete.")
    except subprocess.CalledProcessError as e:
        print(f"Error running mp3_metadata_editor.py: {e}")
    except FileNotFoundError:
        print("Error: mp3_metadata_editor.py not found. Make sure it's in the same directory.")


if __name__ == "__main__":
    print("YouTube to MP3 Downloader and Metadata Editor - Main Script")

    while True:
        print("\nChoose download type:")
        print("1. Download Single Video to MP3")
        print("2. Download Playlist to MP3s")
        print("3. Exit")

        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            run_single_video_downloader()
            run_webm_to_mp4_converter() # Convert WEBM to MP4 after download
            run_mp3_metadata_editor()    # Edit metadata after conversion
        elif choice == '2':
            run_extract_links()
            run_playlist_video_downloader()
            run_webm_to_mp4_converter() # Convert WEBM to MP4 after download
            run_mp3_metadata_editor()    # Edit metadata after conversion
        elif choice == '3':
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

    print("\nAll steps completed.")