from tkinter import *
import datetime
import tkinter as tk 
from tkinter import filedialog
from tkVideoPlayer import TkinterVideo


root = tk.Tk()
root.title("Video Player")
root.geometry("800x700+290+10")



frame = tk.Frame(root)
frame.pack()

image_icon = PhotoImage(file="player.png")
small_image_icon = image_icon.subsample(10) 
root.iconphoto(False, small_image_icon)

lower_frame = tk.Frame(root, bg="#FFFFFF")
lower_frame.pack(fill="both", side=BOTTOM)


def update_duration(event):
    duration = vid_player.video_info()["duration"]
    end_time["text"] = str(datetime.timedelta(seconds=duration))
    progress_slider["to"] = duration

def update_scale(event):
    progress_value.set(vid_player.current_duration())
    

def load_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        vid_player.load(file_path)
        progress_slider.config(to=0, from_=0)
        play_pause_btn["text"] = "Play"
        progress_value.set(0)
        
        
def seek(value):
    vid_player.seek(int(value))
        

def skip(value:int):
    vid_player.seek(int(progress_slider.get())+value)
    progress_value.set(progress_slider.get()+value)
    

def play_pause():
    if vid_player.is_paused():
        vid_player.play()
        play_pause_btn["text"] = "Pause"
    
    else:
        vid_player.pause()
        play_pause_btn["text"] = "Play"
    
def video_ended(event):
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)
    

def video_stop():
    progress_slider.set(progress_slider["to"])
    play_pause_btn["text"] = "Play"
    progress_slider.set(0)
    vid_player.pause()
    


load_button = tk.Button(root,text="Browse", bg="#FFFFFF", font=("calibri",12,"bold"), command=load_video)
load_button.pack(ipadx=12, ipady=4, anchor=tk.NW)

vid_player = TkinterVideo(root, scaled=True)
vid_player.pack(expand=True, fill="both")

buttonback = PhotoImage(file="backward.png")
small_buttonback = buttonback.subsample(11) 
back = tk.Button(lower_frame, image=small_buttonback, bd=0, height=50, width=50, command= lambda:skip(-5)).pack(side= LEFT)

play_pause_btn = tk.Button(lower_frame, text="Play", width=40, height=2, command=play_pause)
play_pause_btn.pack(expand=True, fill="both", side=LEFT)


buttonforward = PhotoImage(file="forward.png")
small_buttonforward = buttonforward.subsample(4) 
playbutton = tk.Button(lower_frame, image= small_buttonforward, bd=0, height=50,width=50, command=lambda: skip(5)).pack(side=LEFT)

buttonstop = PhotoImage(file="stop1.png")
small_buttonstop = buttonstop.subsample(13) 
playbutton = tk.Button(lower_frame, image= small_buttonstop, bd=0, height=50,width=50, command=lambda: video_stop()).pack(side=LEFT)


start_time = tk.Label(root,text = str(datetime.timedelta(seconds=0)))
start_time.pack(side="left")

progress_value = tk.IntVar(root)

progress_slider = tk.Scale(root, variable=progress_value, from_=0 , to=0, orient="horizontal", command=seek)
progress_slider.pack(side="left", fill="x", expand=True)

end_time = tk.Label(root, text = str(datetime.timedelta(seconds=0)))
end_time.pack(side="left")


vid_player.bind("<<Duration>>", update_duration)
vid_player.bind("<<SecondChanged>>", update_scale)

vid_player.bind("<<Ended>>", video_ended)


root.mainloop()