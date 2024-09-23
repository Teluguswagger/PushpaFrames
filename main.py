import tweepy
import os
import re

# Twitter API authentication
consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

# Set up Tweepy v2 client
client = tweepy.Client(consumer_key=consumer_key,
                       consumer_secret=consumer_secret,
                       access_token=access_token,
                       access_token_secret=access_token_secret)

# Set up Tweepy v1.1 API (required for media upload)
auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

# Folder containing the frames in the repository
frames_folder = 'Frames'

# Function to extract the numerical part of the filename
def get_frame_number(filename):
    match = re.search(r'(\d+)', filename)
    return int(match.group()) if match else 0

# List and sort all image files based on their numeric part
frames = sorted(os.listdir(frames_folder), key=get_frame_number)

# File to keep track of the current frame index
current_frame_file = 'current_frame.txt'

# Read the current frame index from the file
try:
    with open(current_frame_file, 'r') as f:
        current_frame = int(f.read().strip())
except FileNotFoundError:
    current_frame = 0

# Total number of frames
total_frames = len(frames)

# Ensure the current frame is valid
if current_frame >= total_frames:
    current_frame = 0  # Reset to the first frame if we've reached the end

# Post the current frame image to Twitter
frame_filename = os.path.join(frames_folder, frames[current_frame])
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
    current_frame += 1

    # Update the current frame index in the file
    with open(current_frame_file, 'w') as f:
        f.write(str(current_frame))

except Exception as e:
    print(f"Error: {e}")
