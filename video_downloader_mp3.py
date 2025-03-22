import yt_dlp
import os
from tqdm import tqdm
from moviepy.audio.io import AudioFileClip
import sys # Import sys module

DEFAULT_MP3_QUALITY = "320k" # Set default MP3 quality here

def download_video_from_url_to_mp3(video_url, download_path=".", mp3_quality=DEFAULT_MP3_QUALITY): # Use default quality
    """
    Downloads a single YouTube video from a URL as an MP3 file using yt-dlp and moviepy.
    MP3 quality is set to DEFAULT_MP3_QUALITY.

    Args:
        video_url: The URL of the YouTube video.
        download_path: The directory to save the MP3 file to (default is current directory).
    """
    ydl_opts = { # ydl_opts remains the same
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
        'progress_hooks': [],
        'noplaylist': True,
        'quiet': True,
    }

    def progress_hook_builder(video_title): # progress_hook_builder remains the same
        pbar = None
        def progress_hook(d):
            nonlocal pbar
            if d['status'] == 'downloading':
                if pbar is None:
                    pbar = tqdm(total=d['total_bytes'] or d['total_bytes_estimate'],
                                unit='B', unit_scale=True, unit_divisor=1024,
                                desc=f"Downloading: {video_title}", initial=d.get('downloaded_bytes', 0), leave=False)
                else:
                    pbar.n = d.get('downloaded_bytes', 0) or pbar.n
                    pbar.total = d['total_bytes'] or d['total_bytes_estimate']
                    pbar.desc = f"Downloading: {video_title}"
                    pbar.update(d['downloaded_bytes'] - pbar.n if 'downloaded_bytes' in d else 0)

            elif d['status'] == 'finished':
                if pbar:
                    pbar.close()
                    print(f"Downloaded: {video_title}")

            elif d['status'] == 'error':
                if pbar:
                    pbar.close()
                    print(f"Error downloading: {video_title}: {d.get('error')}")

        return progress_hook


    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                video_info = ydl.extract_info(video_url, download=False)

                if video_info:
                    video_title = video_info.get('title', 'Unknown Title')

                    if not os.path.exists(download_path):
                        os.makedirs(download_path)

                    try:
                        print(f"\nDownloading audio for video: {video_title}")
                        ydl_opts['progress_hooks'] = [progress_hook_builder(video_title)]
                        filepath = ydl.download([video_url])[0]
                        print(f"Downloaded audio file: {filepath}")

                        # Convert to MP3 using moviepy
                        base, ext = os.path.splitext(filepath)
                        mp3_filepath = base + ".mp3"

                        try:
                            print(f"Converting to MP3 using moviepy: {video_title}")
                            audio_clip = AudioFileClip(filepath)
                            with tqdm(total=1, unit="file", desc=f"Converting to MP3: {video_title}", leave=False) as pbar:
                                audio_clip.write_audiofile(mp3_filepath, bitrate=mp3_quality) # Use DEFAULT_MP3_QUALITY
                                pbar.update(1)
                            audio_clip.close()
                            print(f"Converted to MP3: {mp3_filepath}")

                            # Clean up the original downloaded file (webm, etc.)
                            os.remove(filepath)
                            print(f"Deleted original audio file: {filepath}")

                        except Exception as moviepy_conversion_error:
                            print(f"Error converting to MP3 with moviepy for video '{video_title}': {moviepy_conversion_error}")


                    except Exception as download_error:
                        print(f"Error downloading video: {download_error}")
                else:
                    print(f"Could not retrieve video information for URL: {video_url}")

            except Exception as info_error:
                print(f"Error getting video info: {info_error}")

        print("\nVideo download and conversion process complete!")

    except Exception as main_error:
        print(f"An error occurred: {main_error}")


def download_videos_from_file(links_file="video_links.txt", download_directory=".", mp3_quality=DEFAULT_MP3_QUALITY): # Use default quality
    """
    Reads video URLs from a file and downloads each video as MP3.
    MP3 quality is set to DEFAULT_MP3_QUALITY.

    Args:
        links_file: The file containing video URLs (one URL per line).
        download_directory: The directory to save MP3 files to.
    """
    try:
        with open(links_file, 'r') as f:
            video_links = [line.strip() for line in f if line.strip()] # Read links, remove empty lines

        print(f"Found {len(video_links)} video links in '{links_file}'. Starting downloads...")

        for video_url in tqdm(video_links, desc="Processing videos", unit="video"):
            print(f"\nProcessing URL: {video_url}")
            download_video_from_url_to_mp3(video_url, download_directory, mp3_quality) # Use DEFAULT_MP3_QUALITY

        print("\nAll video downloads from file complete!")

    except FileNotFoundError:
        print(f"Error: Links file '{links_file}' not found.")
    except Exception as e:
        print(f"Error processing video links from file: {e}")


if __name__ == "__main__":
    download_directory = "." # Default download directory
    if "--playlist" in sys.argv: # Check for --playlist flag in command line arguments
        download_directory = sys.argv[-1] if len(sys.argv) > 1 and sys.argv[-1] != "--playlist" else "." # Get directory from argument if provided
        download_videos_from_file(download_directory=download_directory) # Run playlist download
    elif len(sys.argv) > 1: # If there are command line arguments (assume single video URL and optional directory)
        video_url = sys.argv[1] # First argument is video URL
        download_directory = sys.argv[2] if len(sys.argv) > 2 else "." # Second argument (optional) is download directory
        download_video_from_url_to_mp3(video_url, download_directory=download_directory) # Run single video download
    else:
        print("Usage when running video_downloader_mp3.py directly:")
        print("  For single video: python video_downloader_mp3.py <video_url> [download_directory]")
        print("  For playlist (links from video_links.txt): python video_downloader_mp3.py --playlist [download_directory]")