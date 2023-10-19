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
        self.url = "https://www.youtube.com/channel/" + self._channel_id
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
        """Возвращает объект для работы с API, то есть набор ключей и значений."""
        api_key = os.environ.get("youtube_API")
        channel = build('youtube', 'v3', developerKey=api_key)

        return channel

    def to_json(self, json_file):
        """Функция кладет данные экземпляра в указанный json файл."""
        channel_dict = dict(id=self._channel_id,
                            title=self.title,
                            description=self.description,
                            url=self.url,
                            subscriberCount=self.subscriberCount,
                            videoCount=self.video_count,
                            viewCount=self.viewCount)

        with open("moscowpython.json", "w") as file:
            json.dump(channel_dict, file, indent=4)
            file.write("\n")

    # блок с логическими операциями между каналами по количеству подписчиков

    def __str__(self):
        return self.url  # для распечатывания, возвращает ссылку на канал.

    def __add__(self, other):
        return int(self.subscriberCount) + int(other.subscriberCount)    # Сложение

    def __sub__(self, other):
        return int(self.subscriberCount) - int(other.subscriberCount)    # Вычитание

    def __eq__(self, other):
        return int(self.subscriberCount) == int(other.subscriberCount)   # Сравнение

    def __ne__(self, other):
        return int(self.subscriberCount) != int(other.subscriberCount)   # Отрицание

    def __lt__(self, other):
        return int(self.subscriberCount) < int(other.subscriberCount)    # Меньше строгое

    def __gt__(self, other):
        return int(self.subscriberCount) > int(other.subscriberCount)    # Больше строгое

    def __le__(self, other):
        return int(self.subscriberCount) <= int(other.subscriberCount)   # Меньше или равно

    def __ge__(self, other):
        return int(self.subscriberCount) >= int(other.subscriberCount)   # Больше или равно
