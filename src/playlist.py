import datetime
import json
import os

from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    def __init__(self, playlist_id):
        self.__playlist_id = playlist_id
        self.playlist = self.get_service().playlists().list(id=self.__playlist_id,
                                                            part='snippet').execute()['items'][0]
        self.title = self.playlist['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist["id"]}'

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.playlist, indent=2, ensure_ascii=False))

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

            hours, minutes, seconds = "0", "0", "0"
            values = [hours, minutes, seconds]
            time_ = ["H", "M", "S"]

            for key in time_:
                if key in video_obj.duration[2:]:
                    flag = key
                    break

            for symbol in video_obj.duration[2:]:
                for index, key in enumerate(time_):
                    if flag == key:
                        if symbol.isdigit():
                            values[index] += symbol
                        elif index < 2:
                            flag = time_[index + 1]

            hours, minutes, seconds = int(values[0]), int(values[1]), int(values[2])
            video_duration_timedelta = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)

            total_duration += video_duration_timedelta
        return total_duration

    def show_best_video(self):
        videos = self.get_service().playlistItems().list(
            playlistId=self.__playlist_id,
            part='id,contentDetails'
        ).execute()
        max_likes = 0
        # show_best_video = None  # Инициализируем переменную здесь

        for video in videos["items"]:
            video_id = video['contentDetails']['videoId']
            video_obj = Video(video_id)
            # Преобразуем video_obj.like_count в целое число перед сравнением
            video_like_count = int(video_obj.like_count)
            if video_like_count > max_likes:
                max_likes = video_like_count
                url = f"https://youtu.be/{video_id}"
        return url
