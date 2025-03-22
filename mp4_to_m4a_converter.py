from moviepy import *
import os
from tqdm import tqdm

def batch_convert_mp4_to_m4a(delete_mp4=True):
    """
    Batch converts MP4 video files in the current directory to M4A audio format.

    Args:
        delete_mp4: Boolean, if True, delete the original MP4 file after successful conversion (default: True).
    """

    mp4_files_processed = 0
    m4a_files_converted = 0

    for filename in os.listdir('.'):
        if filename.lower().endswith('.mp4'):
            mp4_filepath = filename
            m4a_filepath = os.path.splitext(mp4_filepath)[0] + '.m4a' # Change extension to .m4a
            print(f"Processing MP4 file: {mp4_filepath}")
            mp4_files_processed += 1

            try:
                with tqdm(total=1, unit="file", desc=f"Converting to M4A: {mp4_filepath}", leave=False) as pbar:
                    video_clip = VideoFileClip(mp4_filepath) # Load MP4 video clip
                    audio_clip = video_clip.audio # Extract audio clip
                    audio_clip.write_audiofile(m4a_filepath, codec='aac') # Write audio as M4A (AAC codec)
                    video_clip.close() # Close video clip to release resources
                    audio_clip.close() # Close audio clip to release resources
                    pbar.update(1)
                print(f"  Converted to M4A: {m4a_filepath}")
                m4a_files_converted += 1

                if delete_mp4:
                    os.remove(mp4_filepath)
                    print(f"  Deleted original MP4 file: {mp4_filepath}")

            except Exception as e:
                print(f"  Error converting {mp4_filepath} to M4A: {e}")
                print(f"  Error details: {e}")

    print(f"\nMP4 to M4A conversion process completed.")
    print(f"Total MP4 files found: {mp4_files_processed}")
    print(f"Successfully converted to M4A: {m4a_files_converted}")

if __name__ == "__main__":
    print("MP4 to M4A Batch Converter")
    delete_original = input("Delete original MP4 files after conversion? (yes/no, default: yes): ").strip().lower()
    delete_mp4_files = True if delete_original in ['yes', 'y', ''] else False

    batch_convert_mp4_to_m4a(delete_mp4_files)
    print("\nScript finished.")