import subprocess
import time
from datetime import datetime

# Documentation: Script to record an RTSP stream using FFmpeg

# Parameters:
# - rtsp_link: The RTSP stream URL
# - output_file: Name of the output file where the recording will be saved
# - start_time: Time to start recording (in HH:MM:SS format)
# - end_time: Time to stop recording (in HH:MM:SS format)

# Define the RTSP link and output file
rtsp_link = "rtsp://wowzaec2demo.streamlock.net" # demo RTSP stream
output_file = "recorded_video.mp4"

# Define start and end times
start_time = "18:58:00"
end_time = "18:59:00"

# Function to convert time string to seconds since midnight
def time_to_seconds(time_str):
    """Converts a time string (HH:MM:SS) to seconds since midnight."""
    h, m, s = map(int, time_str.split(":"))
    return h * 3600 + m * 60 + s

# Get the current time and calculate wait time
current_time = datetime.now().strftime("%H:%M:%S")
current_seconds = time_to_seconds(current_time)
start_seconds = time_to_seconds(start_time)
end_seconds = time_to_seconds(end_time)

# Calculate delays
wait_time_start = max(0, start_seconds - current_seconds)
record_duration = max(0, end_seconds - start_seconds)

# Wait until the start time
if wait_time_start > 0:
    print(f"Waiting for {wait_time_start} seconds to start recording...")
    time.sleep(wait_time_start)

# Start recording
print("Starting recording...")
process = subprocess.Popen(
    [
        r"C:\\Users\\yaawa\\Downloads\\ffmpeg-7.0.2-essentials_build\\ffmpeg-7.0.2-essentials_build\\bin\\ffmpeg.exe",
        "-rtsp_transport", "tcp",  # Use TCP for the RTSP stream
        "-i", rtsp_link,
        "-t", str(record_duration),  # Duration of the recording
        "-c:v", "copy",  # Copy video codec without re-encoding
        "-c:a", "aac",   # Re-encode audio to AAC for MP4 compatibility
        output_file
    ],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
)

# Wait for the recording to finish
stdout, stderr = process.communicate()

# Output FFmpeg logs for debugging
print("FFmpeg Output:")
print(stdout.decode())
print("FFmpeg Errors:")
print(stderr.decode())

# Confirm completion
if process.returncode == 0:
    print("Recording completed successfully.")
else:
    print(f"Recording failed with return code {process.returncode}. Check the errors above.")
