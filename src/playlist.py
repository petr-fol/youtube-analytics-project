import json
import os


from googleapiclient.discovery import build


class PlayList:
    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(id=self.__playlist_id, part='snippet').execute()
        self.title = self.playlist['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist["items"][0]["id"]}'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))

    def return_info(self) -> dict:
        """Возвращает информацию о канале."""
        return self.playlist

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с API, то есть набор ключей и значений."""
        api_key = os.environ.get("youtube_API")
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @classmethod
    def total_duration(cls):
