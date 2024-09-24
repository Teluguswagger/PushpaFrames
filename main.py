import tweepy
import os
import glob

# Authentication to Twitter
def twitter_auth():
    API_KEY = os.getenv("TWITTER_API_KEY")
    API_KEY_SECRET = os.getenv("TWITTER_API_SECRET_KEY")
    ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    auth = tweepy.OAuthHandler(API_KEY, API_KEY_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    return tweepy.API(auth)

# Post a frame to Twitter
def post_frame(api, frame_number, total_frames, frame_path):
    tweet_text = f"#Pushpa2Teaser - Frame {frame_number} of {total_frames}"
    api.update_status_with_media(status=tweet_text, filename=frame_path)
    print(f"Posted: {tweet_text}")

# Main function
def main():
    api = twitter_auth()
    
    # Get all frame images from the 'frames' directory
    frames_folder = "frames"
    frames = sorted(glob.glob(f"{frames_folder}/*.[pjPJ][pnNP][gG]*"))  # Match .jpg, .jpeg, .png, .gif

    total_frames = len(frames)
    
    # Track the current frame
    if not os.path.exists("current_frame.txt"):
        current_frame = 0
    else:
        with open("current_frame.txt", "r") as f:
            current_frame = int(f.read().strip())

    if current_frame < total_frames:
        frame_path = frames[current_frame]
        post_frame(api, current_frame + 1, total_frames, frame_path)
        current_frame += 1

        # Update the current frame tracker
        with open("current_frame.txt", "w") as f:
            f.write(str(current_frame))
    else:
        print("All frames have been posted.")

if __name__ == "__main__":
    main()
