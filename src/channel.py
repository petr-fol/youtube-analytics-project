import json
import os

from googleapiclient.discovery import build

from helper.youtube_api_manual import youtube


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self._channel_id = channel_id
        channel = youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.url = channel["items"][0]["snippet"]["thumbnails"]["default"]["url"]
        self.subscriberCount = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.viewCount = channel["items"][0]["statistics"]["viewCount"]

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel, indent=2, ensure_ascii=False))

    def return_info(self) -> dict:
        """Возвращает информацию о канале."""
        channel = youtube.channels().list(id=self._channel_id, part='snippet,statistics').execute()
        return channel

    @classmethod
    def get_service(cls):
        api_key = os.environ.get("youtube_API")
        channel = build('youtube', 'v3', developerKey=api_key)

        return channel

    def to_json(self, json_file):
        channel_dict = dict(id=self._channel_id,
                            title=self.title,
                            description=self.description,
                            url=self.url,
                            subscriberCount=self.subscriberCount,
                            videoCount=self.video_count,
                            viewCount=self.viewCount)

        channel_dict_json = json.dumps(channel_dict)
        with open(json_file, "a") as file:
            file.write(channel_dict_json + "\n")
