import os
import shutil
import tkinter.messagebox

from pytube import YouTube, exceptions
from moviepy.audio.io.AudioFileClip import AudioFileClip

class YouTubeDownloader:

    def __init__(self, youtube_url="", download_path=""):
        self._youtube_url = youtube_url
        self._download_path = download_path


    def update_url(self, youtube_url) -> None:
        self._youtube_url = youtube_url


    def update_download_path(self, download_path) -> None:
        self._download_path = download_path


    def download_mp3(self) -> str | None:
         mp4_path = self.download_mp4()
         if not mp4_path:
             return None
         return self._convert_mp4_to_mp3(mp4_path)


    def download_mp4(self) -> str | None:
        """Downloads a video in .mp4 format based on self._youtube_url.
         The video file will be downloaded to the location of self._download_path
        
        Returns:
               A string representing the mp4's file path or None if unable to download.

        Raises: 
            Exception: if there is any problem with the video/download path or the user decides to cancel their download
            or if the specified download location lacks enough free memory.  

        """
        if not os.path.exists(self._download_path):
            raise Exception("Invalid download path.")
        yt = self._verify_and_get_yt()
        if not yt: 
           return  
        max_attempts = 5
        total_attempts = 0
        while max_attempts > total_attempts : # Occasional exception from KeyError 'streamingData' retrying can fix it.
          try: 
            mp4_file = yt.streams.filter(only_audio=False, only_video=False, 
                                         file_extension="mp4").get_highest_resolution()
            break
          except KeyError as e :
             total_attempts += 1 
        if not mp4_file:
            raise Exception("Unable to querry specific video data.")
        free_bytes = shutil.disk_usage(self._download_path)[2]
        free_gb_str = "\nAvilable: %.1f GB" %(free_bytes / (2**30))
        msg = "Title: " + yt.title + "\n" +"Size: %.1f MB" %mp4_file.filesize_mb + free_gb_str
        confirmation = tkinter.messagebox.askyesno("Confirm download", msg)
        if confirmation: 
            if free_bytes > mp4_file.filesize:
               return mp4_file.download(self._download_path)
            else: raise MemoryError("Not enough memory available.")
        else: 
           raise ValueError("Download canceled")


    def _convert_mp4_to_mp3(self, mp4_path) -> str:
         """
         Converts an MP4 file to an MP3 file format.

         Args:
            mp4_path (str): The file path of the MP4 file to be converted.

         Returns:
            A string representing the MP3 file path.

         Raises:
            Exception: If there is any problem with the file conversion.
         """  
         try:
            mp4_clip = AudioFileClip(filename=mp4_path)
            mp3_path = os.path.splitext(mp4_path)[0] + ".mp3"
            mp4_clip.write_audiofile(filename=mp3_path)
            mp4_clip.close()
            os.remove(mp4_path)
            return mp3_path
         except Exception : 
           os.remove(mp4_path)
           raise Exception("Something went wrong sorry!")
           
           
    def _verify_and_get_yt(self) -> YouTube:
      """Verifies the validity of the YouTube URL and returns a `YouTube` object.

        Returns:
            YouTube: A `YouTube` object representing the video to be downloaded.

        Raises:
            Exception: If the video is age-restricted, region blocked, members-only, private, a live stream,
                unavailable, or if there is an error in the HTML parsing or video extraction will raise a new exception.
                The new exception will have a simpler message compared to the orignal exception that was caught. 
      """
      try:
        youtube = YouTube(self._youtube_url)
        youtube.check_availability()
        if youtube.age_restricted:
            raise Exception("Video is age-restricted.")
        return youtube
      except exceptions.VideoRegionBlocked:
        raise Exception("Video is region blocked.")
      except exceptions.MembersOnly:
        raise Exception("Video is set to members only.")
      except exceptions.RegexMatchError:
        raise Exception("Unable to validate URL.")
      except exceptions.VideoPrivate:
        raise Exception("Unable to download, video is private.")
      except exceptions.LiveStreamError:
        raise Exception("Unable to download, video is a livestream.")
      except exceptions.VideoUnavailable:
        raise Exception("Unable to download, video is unavailable.")
      except exceptions.HTMLParseError:
        raise Exception("Page's HTML had unexpected changes.")
      except exceptions.ExtractError:
        raise Exception("Video extracting error, try again.")