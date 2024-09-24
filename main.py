import os
import tweepy
import re

# Twitter API authentication
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Set up Tweepy v2 client
client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# Set up Tweepy v1.1 API for media upload
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Folder containing the frames in the repository
frames_folder = 'frames'

# Function to extract the numerical part of the filename for sorting
def get_frame_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group()) if match else 0

# List and sort all image files based on their numeric part
frames = sorted(os.listdir(frames_folder), key=get_frame_number)

# File to keep track of the current frame index
current_frame_file = 'current_frame.txt'

# Read the current frame index from the file (default to 0 if file is missing)
try:
    with open(current_frame_file, 'r') as f:
        current_frame = int(f.read().strip())
except (ValueError, FileNotFoundError):
    current_frame = 0  # Start from the first frame if the file doesn't exist or is invalid

# Total number of frames
total_frames = len(frames)

# Ensure the current frame index is within bounds
current_frame = current_frame % total_frames

# Get the current frame filename
frame_filename = os.path.join(frames_folder, frames[current_frame])

# Compose the tweet text
tweet_text = f"#Pushpa2Teaser - Frame {current_frame + 1} of {total_frames}"

try:
    print(f"Attempting to upload image: {frame_filename}")

    # Upload the image using Tweepy v1.1
    media = api.media_upload(frame_filename)
    print("Image uploaded successfully.")

    # Post the tweet with the image using Tweepy v2
    client.create_tweet(text=tweet_text, media_ids=[media.media_id])
    print(f"Posted: {tweet_text} with image: {frame_filename}")

    # Increment the frame index
    next_frame = (current_frame + 1) % total_frames  # Loop back to 0 after the last frame

    # Update the current frame index in the file
    with open(current_frame_file, 'w') as f:
        f.write(str(next_frame))

except Exception as e:
    print(f"Error: {e}")
