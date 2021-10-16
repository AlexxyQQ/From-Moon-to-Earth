import sqlite3
from tkinter import *

import pygame.mixer
from pygame import mixer


def story():
    # Window Configurations
    story_win = Tk()
    story_win.geometry("500x720+0+0")
    story_win.title("From Moon To Earth")
    mixer.init()

    story_win.iconbitmap('Images/icon.ico')

    # Type sound
    sound = pygame.mixer.Sound('Audio/one_type.wav')
    rocket = pygame.mixer.Sound('Audio/rocket.wav')

    def frame1():
        global f1_bg, f1_db

        frame_one = LabelFrame(story_win, width=500, height=720)
        frame_one.place(x=-1, y=-1)

        # Top image
        f1_bg = PhotoImage(file="Images/bgg.png")
        Label(frame_one, image=f1_bg).place(x=0, y=0)

        def database():
            db = sqlite3.connect('Database.db')
            dc = db.cursor()
            valid = True

            try:
                dc.execute('SELECT * FROM Highscores')
                all = dc.fetchall()

                for user in all:
                    if user[0] == users_name.get():
                        Label(frame_one, text='User Already Exist', font=('Arial', 15), bg='black', fg='white').place(
                            x=150, y=610)
                        valid = False

            except:
                pass

            if valid:
                try:
                    dc.execute(""" CREATE TABLE Highscores (player text,highscore text)""")
                    dc.execute(""" INSERT INTO Highscores VAlUES (:p,:h)""", {'p': users_name.get(), 'h': 0})
                    db.commit()
                except:
                    dc.execute(""" INSERT INTO Highscores VAlUES (:p,:h)""", {'p': users_name.get(), 'h': 0})
                    db.commit()

                import global_imports
                global_imports.user_playing = users_name.get()

                frame2()

        def user_name_clear(event):
            if users_name.get() == 'Username':
                users_name.set('')

        users_name = StringVar()
        users_name.set('Username')

        username = Entry(frame_one, text=users_name, font=('Arial', 25))
        username.place(x=65, y=560)
        username.bind('<Button-1>', user_name_clear)

        Button(frame_one, text='Play', command=database, font=('Arial', 15)).place(x=200, y=650)

    def frame2():
        global f2_bg, f2_db, player

        frame_two = LabelFrame(story_win, width=500, height=720)
        frame_two.place(x=-1, y=-1)

        # Top image
        f2_bg = PhotoImage(file="Images/Second Frame Background.png")
        Label(frame_two, image=f2_bg).place(x=0, y=0)

        # Dialog Box
        f2_db = PhotoImage(file="Images/Dialog Box 1.png")
        Label(frame_two, image=f2_db).place(x=0, y=520)

        player = PhotoImage(file="Images/Char 1.png")
        Label(frame_two, image=player, bg='black').place(x=350, y=560)

        Dialog_1 = 'Finally I finished my rocket, now i can go to the Moon to meet the princess.'

        def frame2_d(counter=3):
            l.config(text=Dialog_1[:counter])
            if counter < len(Dialog_1):
                sound.play()
                story_win.after(150, lambda: frame2_d(counter + 1))

            if counter == len(Dialog_1):
                story_win.after(2000, frame3)

        l = Label(frame_two, font=('Arial', 20), wrap=295, bg='black', fg='#e1d147')
        l.place(x=10, y=560)
        frame2_d()

    def frame3():
        global f3_bg, f3_db

        frame_three = LabelFrame(story_win, width=500, height=720)
        frame_three.place(x=-1, y=-1)

        # Top image
        f3_bg = PhotoImage(file="Images/Leaving earth.png")
        Label(frame_three, image=f3_bg).place(x=0, y=0)

        rocket.play()
        story_win.after(4000, frame4)

    def frame4():
        global f4_bg, f4_db, char

        frame_four = LabelFrame(story_win, width=500, height=720)
        frame_four.place(x=-1, y=-1)

        # Top image
        f4_bg = PhotoImage(file="Images/Fourth Frame Background_1.png")
        Label(frame_four, image=f4_bg).place(x=0, y=0)

        # Dialog Box
        f4_db = PhotoImage(file="Images/Dialog Box 1.png")
        Label(frame_four, image=f4_db).place(x=0, y=520)

        char = PhotoImage(file="Images/char_2.png")

        Dialog_1 = 'Beautiful ship you got there, can I ride in it?.'
        Dialog_2 = "Sure M'lady, lets go around the moon."
        Dialog_3 = "Intruder \n He's kidnapping the princess."

        def frame4_d1(counter=3):
            Label(frame_four, image=char, bg='black').place(x=350, y=560)
            l.config(text=Dialog_1[:counter], fg='#26d8c4')
            if counter < len(Dialog_1):
                sound.play()
                story_win.after(150, lambda: frame4_d1(counter + 1))

            if counter == len(Dialog_1):
                story_win.after(400, frame4_d2())

        def frame4_d2(counter=3):
            global char
            char = PhotoImage(file="Images/char 1.png")
            Label(frame_four, image=char, bg='black').place(x=350, y=560)
            l.config(text=Dialog_2[:counter], fg='#e1d147')
            if counter < len(Dialog_2):
                sound.play()
                story_win.after(150, lambda: frame4_d2(counter + 1))

            if counter == len(Dialog_2):
                story_win.after(400, frame4_d3())

        def frame4_d3(counter=3):
            global char, f4_bg
            f4_bg = PhotoImage(file="Images/Fourth Frame Background_2.png")
            Label(frame_four, image=f4_bg).place(x=0, y=0)
            char = PhotoImage(file="Images/cha4_3.png")
            Label(frame_four, image=char, bg='black').place(x=350, y=560)
            l.config(text=Dialog_3[:counter], fg='red')
            if counter < len(Dialog_3):
                sound.play()
                frame_four.after(150, lambda: frame4_d3(counter + 1))

            if counter == len(Dialog_3):
                story_win.after(800, game_start)

        l = Label(frame_four, font=('Arial', 20), wrap=295, bg='black')
        l.place(x=10, y=560)
        frame4_d1()

        def game_start():
            story_win.destroy()
            import Game
            Game.main()

    frame1()

    story_win.mainloop()


if __name__ == '__main__':
    story()
