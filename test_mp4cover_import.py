try:
    from mutagen.mp4 import MP4, MP4Cover
    print("Imported mutagen.mp4 successfully.")
    print(f"Successfully imported MP4: {MP4}")  # Print to confirm MP4 is imported
    print(f"Successfully imported MP4Cover: {MP4Cover}") # Print to confirm MP4Cover is imported
    print("\nIf you see these 'Successfully imported' messages, the basic import is working.")

except ImportError as e:
    print(f"ImportError: Could not import mutagen.mp4 or MP4Cover.")
    print(f"Error details: {e}")
    print("\nThis indicates a problem with your mutagen installation or Python environment.")
    print("Please proceed with reinstalling mutagen and checking your environment.")

except Exception as e:
    print(f"An unexpected error occurred during import test: {e}")
    print("Please report this error if it persists.")

print("\n--- End of Import Test ---")