import subprocess

# Set the starting artist index
START_INDEX = 1625  # Modify this to the last successful artist index

# Run fetch_tracks.py with the starting index as an argument
subprocess.run(["python", "fetch_tracks.py", str(START_INDEX)])
