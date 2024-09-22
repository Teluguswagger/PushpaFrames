import tweepy
import os
from datetime import date, datetime
from datetime import timedelta
from json import dumps

consumer_key = os.environ['TWITTER_API_KEY']
consumer_secret = os.environ['TWITTER_API_SECRET_KEY']
access_token = os.environ['TWITTER_ACCESS_TOKEN']
access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET']

client = tweepy.Client(consumer_key=consumer_key,
                    consumer_secret=consumer_secret,
                    access_token=access_token,
                    access_token_secret=access_token_secret)

# Folder containing the frames in the repository
frames_folder = 'frames'

# List all image files from the frames folder
frames = sorted(os.listdir(frames_folder))

# Read the current frame index from a file
try:
    with open('current_frame.txt', 'r') as f:
        current_frame = int(f.read().strip())
except FileNotFoundError:
    current_frame = 0

# Total number of frames
total_frames = len(frames)

# Post the current frame image to Twitter
if current_frame < total_frames:
    frame_filename = os.path.join(frames_folder, frames[current_frame])
    tweet_text = f"#Pushpa2Teaser - Frame {current_frame + 1} of {total_frames}"

    try:
        # Post the tweet with the image
        api.update_status_with_media(status=tweet_text, filename=frame_filename)
        print(f"Posted: {tweet_text}")
        
        # Increment the frame index
        current_frame += 1
        
        # Update the current frame index in the file
        with open('current_frame.txt', 'w') as f:
            f.write(str(current_frame))
    except Exception as e:
        print(f"Error: {e}")
else:
    print("All frames have been posted.")
