import datetime
import json
import os

from googleapiclient.discovery import build

from src.video import Video


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

    @property
    def total_duration(self):
        total_duration = datetime.timedelta()

        videos = self.get_service().playlistItems().list(
            playlistId=self.__playlist_id,
            part='id,contentDetails'
        ).execute()

        for video in videos['items']:
            video_id = video['contentDetails']['videoId']

            # Инициализируем объект Video для получения информации о видео
            video_obj = Video(video_id)

            # Получаем длительность видео с помощью объекта Video
            video_duration = video_obj.duration

            hours, minutes, seconds = "0", "0", "0"
            if "H" in video_duration[2:]:
                flag = "H"
            elif "M" in video_duration[2:]:
                flag = "M"
            else:
                flag = "S"

            for symbol in video_duration[2:]:

                if flag == "H":
                    if symbol.isdigit():
                        hours += symbol
                    else:
                        flag = "M"

                if flag == "M":
                    if symbol.isdigit():
                        minutes += symbol
                    else:
                        flag = "S"

                if flag == "S":
                    if symbol.isdigit():
                        seconds += symbol

            hours, minutes, seconds = int(hours), int(minutes), int(seconds)
            video_duration_timedelta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

            total_duration += video_duration_timedelta
        return total_duration

    def show_best_video(self):
        videos = self.get_service().playlistItems().list(
            playlistId=self.__playlist_id,
            part='id,contentDetails'
        ).execute()
        popular_video_id = 0
        max_likes = 0
        # show_best_video = None  # Инициализируем переменную здесь

        for video in videos["items"]:
            video_obj = Video(video["contentDetails"]["videoId"])
            # Преобразуем video_obj.like_count в целое число перед сравнением
            video_like_count = int(video_obj.like_count)
            if video_like_count > max_likes:
                max_likes = video_like_count
                url = f"https://youtu.be/{video['contentDetails']['videoId']}"
        return url
