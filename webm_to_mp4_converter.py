import os
import subprocess
from tqdm import tqdm


def batch_convert_webm_to_mp4_ffmpeg_direct(delete_webm=True):
    """
    Batch converts WEBM video files in the current directory to MP4 format
    using direct ffmpeg command execution via subprocess.

    Args:
        delete_webm: Boolean, if True, delete the original .webm file after successful conversion (default: True).
    """

    webm_files_processed = 0
    webm_files_converted = 0

    for filename in os.listdir('.'):
        if filename.lower().endswith('.webm'):
            webm_filepath = filename
            mp4_filepath = os.path.splitext(webm_filepath)[0] + '.mp4' # Change extension to .mp4
            print(f"Processing WEBM file: {webm_filepath}")
            webm_files_processed += 1

            try:
                with tqdm(total=1, unit="file", desc=f"Converting to MP4: {webm_filepath}", leave=False) as pbar:
                    # Construct the ffmpeg command
                    command = [
                        "ffmpeg",
                        "-i", webm_filepath,  # Input file
                        "-codec:v", "libx264", # Video codec
                        "-codec:a", "aac",    # Audio codec
                        "-strict", "experimental", # or "normal" or "unofficial" - try "experimental" first
                        mp4_filepath          # Output file
                    ]

                    # Execute the ffmpeg command using subprocess.run
                    result = subprocess.run(command, capture_output=True, text=True, check=True)

                    pbar.update(1)
                print(f"  Converted to MP4: {mp4_filepath}")
                webm_files_converted += 1

                if delete_webm:
                    os.remove(webm_filepath)
                    print(f"  Deleted original WEBM file: {webm_filepath}")

            except subprocess.CalledProcessError as e:
                print(f"  Error converting {webm_filepath}: ffmpeg command failed.")
                print(f"  Return code: {e.returncode}")
                print(f"  Stdout: {e.stdout}")
                print(f"  Stderr: {e.stderr}")
                print("  Check ffmpeg output for details.")

            except FileNotFoundError:
                print("  Error: ffmpeg command not found. Make sure ffmpeg is installed and in your system's PATH.")

            except Exception as e: # Catch any other unexpected errors
                print(f"  An unexpected error occurred while processing {webm_filepath}: {e}")
                print("  Please report this error with details if it persists.")


    print(f"\nWEBM to MP4 conversion process completed (using direct ffmpeg commands).")
    print(f"Total WEBM files found: {webm_files_processed}")
    print(f"Successfully converted to MP4: {webm_files_converted}")

if __name__ == "__main__":
    print("WEBM to MP4 Batch Converter (Direct ffmpeg Command Execution)")
    delete_original = input("Delete original WEBM files after conversion? (yes/no, default: yes): ").strip().lower()
    delete_webm_files = True if delete_original in ['yes', 'y', ''] else False

    batch_convert_webm_to_mp4_ffmpeg_direct(delete_webm_files)
    print("\nScript finished.")