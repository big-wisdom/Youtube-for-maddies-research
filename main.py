import csv
import json
import urllib

from googleapiclient.discovery import build


def get_video_id(youtube_url):
    """Gets the video ID from the YouTube URL."""

    parsed_url = urllib.parse.urlparse(youtube_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    video_id = query_params['v'][0]

    return video_id


# Get the YouTube API service object
youtube = build('youtube', 'v3', developerKey="")

# Get the comments for the video
comments = youtube.comments().list(part='snippet', videoId="U8U_gR58eJU").execute()
# comments = youtube.comments().list(part='snippet', videoId="U8U_gR58eJU").execute()

# Write the comments to a CSV file
# with open('comments.csv', 'w', encoding='utf-8') as csvfile:
#     fieldnames = ['comment_id', 'author_name', 'text', 'likes', 'kind', 'id', 'snippet', 'etag']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for comment in comments['items']:
#         writer.writerow(comment)
for comment in comments['items']:
    print(comment['snippet']['topLevelComment']['snippet']['textDisplay'])
