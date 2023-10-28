import json

from googleapiclient.discovery import build
import os


class Video:

    def __init__(self, video_id):
        self.__video_id = video_id
        self.video = self.get_service().videos().list(part='snippet,statistics, contentDetails', id=self.__video_id).execute()
        self.title = self.video['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']
        self.duration = self.video['items'][0]['contentDetails']['duration']

    @classmethod
    def get_service(cls):
        api_key = os.environ.get("youtube_API")
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.video, indent=2, ensure_ascii=False))

    def __str__(self):
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        super().__init__(video_id)
        self.__video_id = video_id
        self.playlist_id = playlist_id
