from tkinter import *
import pygame
import os
import threading
import time
from mutagen.mp3 import MP3
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showerror,askquestion,showinfo
from tkinter import ttk
from PIL import Image,ImageTk

class player:
    
    #Make the constructor
    def __init__(self,master):
        self.master=master #Now master in this class is the root
        pygame.init()
        pygame.mixer.init()
        
        def get_icon():
            self.winicon=PhotoImage(file="icon.png")
            master.iconphoto(False,self.winicon)
        def icon():
            threads=threading.Thread(target=get_icon)
            threads.start()
        icon()
        PLAY = "►"
        PAUSE = "║║"
        PREV = "⏮"
        NEXT = "⏭"
        STOP = "■"
        UNPAUSE = "||"
        mute = "🔇"
        unmute = u"\U0001F50A"
        vol_mute = 0.0
        vol_unmute = 1
        
        #Listbox that carry  the list of the songs.
        self.scroll=Scrollbar(master)
        self.play_list=Listbox(master,font=("sansarif",12,"bold"),bd=4,width=38,height=19,bg="white",fg="black",selectbackground="Black")
        self.play_list.place(x=600,y=77)
        self.scroll.place(x=946,y=80,height=389,width=15)
        self.scroll.config(command=self.play_list.yview)
        self.play_list.config(yscrollcommand=self.scroll.set)
        
        #palcing the image 
        self.img=PhotoImage(file="image2.png",height=480,width=600)
        self.img_lab=Label(master,image=self.img)
        self.img_lab.grid()
        self.img_lab["compound"]=LEFT
        
        #It will show which song is playing 
        self.var=StringVar()
        self.var.set("-------------------------------------------------------------------")
        self.song_title=Label(master,font=("Times new roman",12,"bold"),bg="black",fg="white",textvariable=self.var,width=70)
        self.song_title.place(x=3,y=0)
        #=================Defining the Function ======================================================
        
        def addSongs():
            try:
                directory=askdirectory()
                os.chdir(directory)
                song_list=os.listdir()
                song_list.reverse()
                
                for song in song_list:
                    pos=0
                    if song.endswith(('mp3')):
                        self.play_list.insert(pos,song)
                        pos+=1
                    index=0
                    self.play_list.selection_set(index)
                    self.play_list.see(index)
                    self.play_list.activate(index)
                    self.play_list.select_anchor(index)
            except:
                showerror("File selection error !! please select the file correctly")
        
        def add_songs_playlist():
            threads=threading.Thread(target=addSongs)
            threads.start()
        def get_time():
            current_time=pygame.mixer.music.get_pos() /1000  #Here we get the time of the  current running song
            formatted_curent_time=time.strftime("%H:%M:%S",time.gmtime(current_time))
            next_one= self.play_list.curselection()
            song=self.play_list.get(next_one)
            song_x=MP3(song)
            song_length=int(song_x.info.length)
            formated_length=time.strftime("%H:%M:%S",time.gmtime(song_length))
            self.label_time.config(text=f"{formatted_curent_time}/{formated_length}")
            self.progress["maximum"]=song_length   #The max the progress pbar can go upto the length of the song 
            self.progress["value"]=int(current_time)  #we can  set the progress value to the current time we have  
            
            master.after(100,get_time) # Here after every second we update the function
        def play_music():
            try:
                track=self.play_list.get(ACTIVE)
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
                get_time()
            except:
                showerror("No music ! Load the music you want to play")
        def play_thread():
            threads=threading.Thread(target=play_music)
            threads.start()
        # master.bind("<pace>",lambda x:play_thread())
        
        #Function for repeat
        def repeat():
            try:
                index=0
                self.play_list.select_clear(0,END)
                self.play_list.selection_set(index,last=None) #Here we set our selection of the song in the index position
                self.play_list.see(index) #Here we can see the Index song 
                self.play_list.activate(index) #Here  the song in the index will be activate 
                self.play_list.select_anchor(index)
                track=self.play_list.get(index) #Hrere we get the track from our paly list
                pygame.mixer.music.load(track)
                self.var.set(track)
                pygame.mixer.music.play()
            
            except:
                showerror("No song in the Play Lists ! Plase add the songs ")
        def repeat_thread():
            threads=threading.Thread(target=repeat)
            threads.start()
            
        #Function for pause and unpause the 
        def pause_unpause():
            
            if self.pause['text']== PAUSE:
                pygame.mixer.music.pause()
                self.pause['text']=UNPAUSE
            else:
                pygame.mixer.music.unpause()
                self.pause['text']=PAUSE
        
       
        
        
        #for stop the music
        def stop():
            pygame.mixer.music.stop()
        
        #for set the volume
        def volume(x):
            pygame.mixer.music.set_volume(self.volume_slider.get())
            
        #Function for mute and unmute
            
        def muted():
            if self.mute['text']==unmute:
                pygame.mixer.music.set_volume(vol_mute)
                self.mute['text']= mute
                self.volume_slider.set(vol_mute)
                self.mute['fg']="red"
            elif self.mute['text']==mute:
                pygame.mixer.music.set_volume(vol_unmute)
                self.volume_slider.set(vol_unmute)
                self.mute['fg']='white'
                self.mute['text']=unmute
        # Function for the paly the next song
        
        def next_song():
            curr=self.play_list.curselection()
            next_one=curr[0]+1 #It will give the index of next song of what song is palying
            song=self.play_list.get(next_one)   #Here we get the next song
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.play_list.select_clear(0,END)
            self.play_list.selection_set(next_one,last=None)
            self.play_list.see(next_one)
            self.play_list.activate(next_one)
            self.play_list.select_anchor(next_one)
            
            self.var.set(song)
            get_time()
        def next():
            threads=threading.Thread(target=next_song)
            threads.start()
        master.bind("<Left>",next)
        
        def prev_song():
            curr=self.play_list.curselection()
            prev_one=curr[0]-1 #It will give the index of next song of what song is palying
            song=self.play_list.get(prev_one)   #Here we get the next song
            pygame.mixer.music.load(song)
            pygame.mixer.music.play()
            self.play_list.select_clear(0,END)
            self.play_list.selection_set(prev_one,last=None)
            self.play_list.see(prev)
            self.play_list.activate(prev_one)
            self.play_list.select_anchor(prev_one)
            
            self.var.set(song)
            get_time()
            
        def prev():
            threads=threading.Thread(target=prev_song)
            threads.start()
        
       
        
        def exit():
            msgbox= askquestion('Exit Application','Are You Sure To Exit the Application',icon="warning")
            
            if msgbox =="yes":
                master.quit()
                master.after(100,exit)
            else:
                showinfo('Return','Continue Playing your awosome music')
            return
        def help():
            top=Toplevel()
            top.title("Help")
            top.geometry("350x554+500+80")
            top.resizable(width=0,height=0)
            user_manual=[
                "Music Player Manual :\n",
                'PLAY = "►"',
                'PAUSE = "║║" ',
                'PREV = "⏮" ',
                'NEXT = "⏭" ',
                'STOP = "■" ',
                'UNPAUSE = "||" ',
                'mute = "🔇" ',
                'unmute = u"\U0001F50A" '
            ]
            
            for i in user_manual:
                manual=Label(top,text=i,width=50,height=3,bg="black",fg="White")
                manual.pack(side=TOP, fill="both")
            
            
            
            
        
                
        
        
                
            
                
            
        
        
        
        #==== add the help and exit to the menu 
        self.menu=Menu(self.img_lab,font="sansarif,3")
        master.config(menu=self.menu)
        self.menu.add_command(label="HELP",command=help)
        self.menu.add_command(label="EXIT",command=exit)
        
        #Draw a  separtor line 
        
        self.separator=ttk.Separator(self.img_lab,orient='horizontal')
        self.separator.place(relx=0,rely=0.85,relwidth=1,relheight=1)
        
        #Making the buttons 
        self.play=Button(master,text=PLAY,width=4,bd=5,font="Helvertica,15",bg='black',fg="white",command=play_thread)
        self.play.place(x=150,y=420)
        
        self.stop=Button(master,text=STOP,width=4,bd=5,font="Helvertica,15",bg='black',fg="white",command=stop)
        self.stop.place(x=225,y=420)
        
        self.prev=Button(master,text=PREV,width=4,bd=5,font="Helvertica,15",bg='black',fg="white",command=prev)
        self.prev.place(x=10,y=420)
         
        self.next=Button(master,text=NEXT,width=4,bd=5,font="Helvertica,15",bg='black',fg="white",command=next)
        self.next.place(x=295,y=420)
        
        self.pause=Button(master,text=PAUSE,width=4,bd=5,font="Helvertica,15",bg='black',fg="white",command=pause_unpause)
        self.pause.place(x=85,y=420)
        
        self.mute=Button(master,text=unmute,width=4,bd=5,font="Helvertica,15",bg='black',fg="white",command=muted)
        self.mute.place(x=430,y=420)
        
        self.repeat=Button(master,text="\U0001F501",width=4,bd=5,font="Helvertica,15",bg='black',fg="white",command=repeat_thread)
        self.repeat.place(x=375,y=420)
        
        self.load_music=Button(master,text="!!click here to brwose the song!!",bg="black",fg="white",width=47,bd=4,command=add_songs_playlist)
        self.load_music.place(x=606,y=82)
        
        #Making a style object that will help in volume slider .
        self.style=ttk.Style()
        self.style.configure("myStyle.Horizontal.TScale",background="#505050")
        
        #Making the sound slider.
        self.volume_slider= ttk.Scale(self.img_lab,from_=0,to=1,orient=HORIZONTAL,length=100,value=1,style="myStyle.Horizontal.TScale",command=volume)
        self.volume_slider.place(x=477,y=425)
        
        #making the progress bar
        
        self.progress=ttk.Progressbar(self.img_lab,value=0,mode="determinate",orient=HORIZONTAL,cursor='spider',length=453)
        self.progress.place(x=10,y=385)
        
        #Creating a label for the showing the time
        self.label_time=Label(master,text="00:00:00 / 00:00:00",font=("Helvetica",12),width=15,bg="black",fg='white')
        self.label_time.place(x=460,y=387)
        
        #Label  for showing where is our  paly list is .
        
        self.label_playlist=Label(master,text="!! Music PlayList !!",font=("Helvetica",18),fg="black",bd=2,width=30,bg="white")
        self.label_playlist.place(x=615,y=14)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
        
        
        
        # =====add a music list to the listbox======
        
        
        
        
        
        
def main():
    root=Tk()
    ui=player(root)
    root.geometry("963x470+200+100")
    root.title("MyMusicPlayer")
    root.configure(bg="Black")
    root.resizable(width=0,height=0)
    
    root.mainloop()
    
if __name__=="__main__":
    main()