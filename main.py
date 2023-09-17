import csv
import json
import urllib

from googleapiclient.discovery import build

# Every day I want to just open my laptop and run this program and let it add all the comments that it can.


def get_video_id(youtube_url):
    """Gets the video ID from the YouTube URL."""

    parsed_url = urllib.parse.urlparse(youtube_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    video_id = query_params['v'][0]

    return video_id


def query_comments(video_id, youtube, next_page_token):
    # Get the comments for the video
    request = youtube.commentThreads().list(
        part="snippet",
        maxResults=100,
        textFormat="plainText",
        videoId=video_id,
        pageToken=next_page_token
    )
    return request.execute()


def main():
    # get developer key and video URL from config file
    with open("config.json") as json_data_file:
        config_data = json.load(json_data_file)

    # Get the YouTube API service object
    youtube = build('youtube', 'v3', developerKey=config_data['developer-key'])

    # query for comments
    video_id = get_video_id(config_data['video-url'])

    while True:
        response = query_comments(video_id, youtube, config_data['next-page-token'])

        # Write nextPageToken to the config file
        config_data['next-page-token'] = response['nextPageToken']
        with open("config.json", "w") as outfile:
            json.dump(config_data, outfile)

        # Filter data
        filtered_data = [
            {
                'id': item['id'],
                'text': item['snippet']['topLevelComment']['snippet']['textOriginal'],
                'publishedAt': item['snippet']['topLevelComment']['snippet']['publishedAt'],
                'authorDisplayName': item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            }
            for item in response['items']
        ]

        # write comments to csv
        csv_filename = "comments.csv"

        # Open the CSV file in append mode ('a') to add data to the end
        with open(csv_filename, mode="a", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=["id", "text", "publishedAt", "authorDisplayName"])

            # If the file is empty, write the header row
            if csv_file.tell() == 0:
                writer.writeheader()

            # Write the data to the CSV file
            writer.writerows(filtered_data)


if __name__ == "__main__":
    main()
