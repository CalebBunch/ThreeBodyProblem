from threading import Thread
from time import sleep
from tkinter import *
root = Tk()

def k(arg):
    global root
    l = Label(root)
    l.pack()

    e = Entry(root)
    e.pack()
    
    def submit():
        l.configure(text = e.get())

    Button(text="Submit",command=submit).pack()
    
    
i = 0
def threaded_function(arg):
    global i
    while True:
        print(i)
        i+=1
        sleep(1)
        

if __name__ == "__main__":
    thread2 = Thread(target = k, args = (12,))
    thread = Thread(target = threaded_function, args = (12,))
    thread2.start()
    thread.start()

    root.mainloop()
