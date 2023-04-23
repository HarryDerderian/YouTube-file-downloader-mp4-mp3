from time import sleep
from threading import Thread
from tkinter import Tk, Frame, Label, Entry, Button, messagebox
from tkinter.ttk import Progressbar

from youtube_downloader import YouTubeDownloader

class YouTubeToMp3:
    _MAIN_BACKGROUND_COLOR = "black"
    _TEXT_COLOR = "white"
    _SECOND_BACKGROUND_COLOR = "#5A5A5A"
    _TITLE = "YouTube to mp3"
    _WIDTH = 700
    _HEIGHT = 350
    _HEIGHT_RESIZABLE = False
    _WIDTH_RESIZABLE = False
    _HEADER_FONT = ("Roboto", 30)
    _MAIN_FONT = ("Arial", 15)
    _INPUT_BAR_WIDTH = 45
    _BUTTON_WIDTH = 20
    _BUTTON_HEIGHT = 1
    
    
    def __init__(self) :
        # Download logic 
        self._downloader = YouTubeDownloader()
        self._download_in_progress = False

        # Build the G.U.I. piece by piece.
        self._build_root()
        self._build_main_window()
        self._build_labels()
        self._build_text_inputs()
        self._build_download_mp3_button()
        self._build_download_mp4_button()
        self._build_progress_bar()
        
        # Display and run the G.U.I.
        self._root.mainloop()


    def _build_root(self) :
        self._root = Tk()
        self._root.title(self._TITLE)
        self._root.geometry(str(self._WIDTH) + "x" + str(self._HEIGHT))
        self._root.resizable(self._WIDTH_RESIZABLE, self._HEIGHT_RESIZABLE)


    def _build_main_window(self) :
        self._main_window = Frame(self._root, 
                            bg = self._MAIN_BACKGROUND_COLOR, 
                            height = self._HEIGHT, width = self._WIDTH)
        self._main_window.place(x = 0, y = 0) 


    def _build_labels(self) :
        # HEADER
        self._title = Label(self._main_window, text = "YouTube Downloader",
                      fg = self._TEXT_COLOR, bg = self._MAIN_BACKGROUND_COLOR,
                      font = self._HEADER_FONT)
        self._title.place(x =175, y = 10)
        
        # URL LABEL
        url_label = Label(self._main_window, text="YouTube URL:  ", 
                          bg = self._MAIN_BACKGROUND_COLOR, fg = self._TEXT_COLOR,
                          font = self._MAIN_FONT)
        url_label.place(x = 10, y = 115)
        
        # DOWNLOAD PATH LABEL
        self._download_path_label = Label(self._main_window,text="Download path: ", 
                                          bg = self._MAIN_BACKGROUND_COLOR, fg = self._TEXT_COLOR,
                                          font = self._MAIN_FONT)
        self._download_path_label.place(x = 0, y = 200)

        # PROGRESS BAR LABEL
        self._downloading_label = Label(self._main_window,text="Download progress", 
                                          bg = self._MAIN_BACKGROUND_COLOR, fg = self._TEXT_COLOR,
                                          font = self._MAIN_FONT)
        self._downloading_label.place(x=105, y = 260)

    def _build_text_inputs(self) :
        # URL INPUT
        self._url_input = Entry(self._main_window, width = self._INPUT_BAR_WIDTH,
                                bg = self._SECOND_BACKGROUND_COLOR,
                                fg = self._TEXT_COLOR, font = self._MAIN_FONT)
        self._url_input.place(x = 145, y = 115)
        
        # DOWNLOAD PATH INPUT
        self._file_path_input = Entry(self._main_window, width = self._INPUT_BAR_WIDTH, 
                                      bg = self._SECOND_BACKGROUND_COLOR,
                                      fg = self._TEXT_COLOR, font = self._MAIN_FONT)
        self._file_path_input.place(x = 145, y = 200)


    def _build_download_mp3_button(self) :
        self._get_mp3_button = Button(self._main_window,
                                      bg = self._SECOND_BACKGROUND_COLOR, 
                                      fg = self._TEXT_COLOR, text = "Download Audio 🢂 .mp3", 
                                      width = self._BUTTON_WIDTH, height =self._BUTTON_HEIGHT,
                                      font = self._MAIN_FONT,
                                      command = lambda: Thread(target=self._download_mp3).start())
        self._get_mp3_button.place(x=450,y=250)
    

    def _build_download_mp4_button(self) :
    
        self._get_mp4_button = Button(self._main_window, 
                                      bg = self._SECOND_BACKGROUND_COLOR, 
                                      fg = self._TEXT_COLOR, text = "Download Video 🢂 .mp4", 
                                      width = self._BUTTON_WIDTH, height =self._BUTTON_HEIGHT,
                                      font = self._MAIN_FONT,
                                      command = lambda: Thread(target=self._download_mp4).start())
        self._get_mp4_button.place(x = 450, y= 300)


    def _download_mp3(self) :
        if self._download_in_progress : return
        self._download_in_progress = True
        self._get_mp3_button.config(state="disabled")
        self._get_mp4_button.config(state="disabled")
        self._downloader.update_url(self._url_input.get())
        self._downloader.update_download_path(self._file_path_input.get().strip('\"'))
        try :
            Thread(target=self._update_current_progress).start()
            filepath = self._downloader.download_mp3()
            self._download_in_progress = False
            messagebox.showinfo(title="Success!", message="video has been downloaded to: " + filepath)
        except Exception as e:
            self._download_in_progress = False
            messagebox.showerror(title="Error downloading audio.", message=str(e))
        self._get_mp3_button.config(state="normal")
        self._get_mp4_button.config(state="normal")


    def _download_mp4(self) :
        if self._download_in_progress : return
        self._download_in_progress = True
        self._get_mp3_button.config(state="disabled")
        self._get_mp4_button.config(state="disabled")
        self._downloader.update_url(self._url_input.get())
        self._downloader.update_download_path(self._file_path_input.get().strip('\"'))
        try :
             Thread(target=self._update_current_progress).start()
             filepath = self._downloader.download_mp4()
             self._download_in_progress = False
             messagebox.showinfo(title="Success!", message="video has been downloaded to: " + filepath)
        except Exception as e :
            self._download_in_progress = False
            messagebox.showerror(title="Error downloading video.", message=str(e))
        self._get_mp3_button.config(state="normal")
        self._get_mp4_button.config(state="normal")
        

    def _build_progress_bar(self) :
        self._progressbar = Progressbar(orient="horizontal",length = 350, value=100, mode = "determinate")
        self._progressbar.place(x=50, y =290)
    

    def _update_current_progress(self):
        self._progressbar["value"] = 0
        i = 13
        while self._download_in_progress:
            if self._progressbar["value"] >= 50 :
                i = 2
            if self._progressbar["value"] >= 80 :
                i = 1
            if self._progressbar["value"] >= 95 :
                i = 0.1
            if self._progressbar["value"] >= 99 :
                i = 0          
            self._progressbar["value"] += i
            self._downloading_label.config(text= "Download progress: " +str("%.2f"%self._progressbar["value"]) +"%" )
            self._root.update_idletasks()
            sleep(1)
        self._progressbar["value"] = 100
        self._downloading_label.config(text= "Download complete!")