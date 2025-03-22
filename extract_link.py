from pytube import Playlist
import sys # Import sys
import os

def extract_playlist_links(playlist_url, output_file="video_links.txt"):
    """
    Extracts video URLs from a YouTube playlist and saves them to a file.

    Args:
        playlist_url: The URL of the YouTube playlist.
        output_file: The name of the file to save video URLs to (default: "video_links.txt").
    """
    try:
        playlist = Playlist(playlist_url)
        video_urls = playlist.video_urls

        with open(output_file, 'w+') as f:
            for url in video_urls:
                f.write(url + '\n')

        print(f"Extracted {len(video_urls)} video links from playlist and saved to '{output_file}'")

    except Exception as e:
        print(f"Error extracting playlist links: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1: # Check for command line argument
        playlist_link = sys.argv[1] # Get playlist URL from command line argument
        extract_playlist_links(playlist_link)
    else:
        print("Usage when running extract_link.py directly:")
        print("  python extract_link.py <playlist_url>")