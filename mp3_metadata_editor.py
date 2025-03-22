from mutagen import File # Import general File function
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4, MP4Cover  # Import MP4 for m4a
from mutagen.id3 import ID3, TIT2, TPE1, TPE2, TALB, APIC, TCON
import os

SUPPORTED_EXTENSIONS = ['.mp3', '.m4a', '.mp4'] # ADDED .mp4 to supported extensions

def batch_edit_audio_metadata(artist_name, album_name, genre_name, artwork_filename="artwork.jpg"):
    """
    Batch edits metadata for MP3, M4A, and MP4 audio files in the current directory.
    WEBM files are skipped. Now includes MP4 support.

    Args:
        artist_name: The artist name to set for all audio files.
        album_name: The album name to set for all audio files.
        genre_name: The genre name to set for all audio files.
        artwork_filename: The filename of the artwork image (default: "artwork.jpg").
                          It should be in the same directory as the script.
                          Supports "artwork.jpg" and "artwork.png".
    """

    artwork_path = None
    if os.path.exists(artwork_filename):
        artwork_path = artwork_filename
    elif os.path.exists("artwork.png"):
        artwork_path = "artwork.png"
    else:
        print("Artwork file 'artwork.jpg' or 'artwork.png' not found in the current directory. No artwork will be added.")

    audio_files_processed = 0

    for filename in os.listdir('.'):
        file_extension = os.path.splitext(filename)[1].lower()
        if file_extension in SUPPORTED_EXTENSIONS: # Check against supported extensions (now includes .mp4)
            audio_filepath = filename
            print(f"Processing audio file: {audio_filepath}")

            try:
                audio = File(audio_filepath) # Use mutagen.File to detect file type

                if not audio: # mutagen.File might return None if it can't handle the file
                    print(f"  Skipping: Unrecognized or unsupported audio format for '{audio_filepath}'")
                    continue # Skip to the next file

                # Ensure tags exist - this is more general now
                if audio.tags is None:
                    print("  No existing tags found, creating new tags.")
                    if file_extension == '.mp3':
                        audio.tags = ID3() # Create ID3 tags for MP3
                    elif file_extension == '.m4a' or file_extension == '.mp4': # Also create MP4 tags for .mp4
                        audio.tags = MP4() # Create MP4 tags for M4A and MP4
                    else: # For webm and potentially others, let mutagen.File handle tag creation if possible.
                        pass # Rely on mutagen.File to initialize tags appropriately if needed.

                # Set Artist, Album, and Genre (using ID3 tags for simplicity - might work for m4a too)
                audio.tags['TPE1'] = TPE1(encoding=3, text=artist_name) # Artist
                audio.tags['TPE2'] = TPE2(encoding=3, text=artist_name) # Album Artist
                audio.tags['TALB'] = TALB(encoding=3, text=album_name) # Album
                audio.tags['TCON'] = TCON(encoding=3, text=genre_name) # Genre

                # Set Artwork if available (format-specific handling)
                if artwork_path:
                    with open(artwork_path, 'rb') as img_file:
                        artwork_data = img_file.read()
                        mime_type = 'image/jpeg' if artwork_path.lower().endswith('.jpg') else 'image/png'

                        if file_extension == '.mp3':
                            audio.tags['APIC:'] = APIC( # Use APIC for MP3
                                encoding=3,
                                mime=mime_type,
                                type=3,
                                desc=u'Cover',
                                data=artwork_data
                            )
                        elif file_extension == '.m4a' or file_extension == '.mp4': # Also use MP4Cover for .mp4
                            # Use MP4Cover for M4A/MP4 artwork
                            image_format = MP4Cover.FORMAT_JPEG if mime_type == 'image/jpeg' else MP4Cover.FORMAT_PNG
                            audio.tags['covr'] = [MP4Cover(artwork_data)] # Assign a list of MP4Cover objects


                    print(f"  Artwork added from '{artwork_path}'")
                else:
                    print("  No artwork added.")

                audio.save() # Save the changes
                audio_files_processed += 1
                print(f"  Metadata updated for: {audio_filepath}")

            except Exception as e:
                print(f"  Error processing {audio_filepath}: {e}")

    print(f"\nMetadata update process completed.")
    print(f"Successfully processed {audio_files_processed} audio files.")

if __name__ == "__main__":
    artist = input("Enter the Artist Name for all audio files: ")
    album = input("Enter the Album Name for all audio files: ")
    genre = input("Enter the Genre for all audio files: ")

    print(f"\nSetting Artist: '{artist}', Album: '{album}', Genre: '{genre}' and adding artwork (if found).")
    batch_edit_audio_metadata(artist, album, genre)
    print("\nScript finished.")