import json
from googleapiclient.discovery import build
import os


class Video:
    def __init__(self, video_id):
        """
        Конструктор класса Video.

        Args:
            video_id (str): Идентификатор видео.

        """
        self.__video_id = video_id
        try:
            self.video = self.get_service().videos().list(part='snippet,statistics, contentDetails',
                                                          id=self.__video_id).execute()['items'][0]

        except IndexError:
            # Если возникает IndexError, обрабатываем исключение
            self.video, self.title, self.url, self.view_count, self.like_count, self.duration\
                = None, None, None, None, None, None
            print("Запрос к API вернул пустые поля")

        else:
            # Если исключение не возникает, устанавливаем значения атрибутов
            self.title = self.video['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.__video_id}"
            self.view_count = self.video['statistics']['viewCount']
            self.like_count = self.video['statistics']['likeCount']
            self.duration = self.video['contentDetails']['duration']

    @classmethod
    def get_service(cls):
        """
        Создает и возвращает экземпляр объекта YouTube API.

        Returns:
            googleapiclient.discovery.Resource: Экземпляр объекта YouTube API.

        """
        api_key = os.environ.get("youtube_API")
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def print_info(self) -> None:
        """Выводит в консоль информацию о видео."""
        print(json.dumps(self.video, indent=2, ensure_ascii=False))

    def __str__(self):
        """
        Возвращает строковое представление объекта Video.

        Returns:
            str: Заголовок видео.

        """
        return self.title


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """
        Конструктор класса PLVideo.

        Args:
            video_id (str): Идентификатор видео.
            playlist_id (str): Идентификатор плейлиста.

        """
        super().__init__(video_id)
        self.__video_id = video_id
        self.playlist_id = playlist_id
