import tkinter as tk
root=tk.Tk()
root.title("learining frames")
root.geometry("700x400")



def printName():
    tk.Label(root,text="Hello Ankit!", fg='green').pack()
    

f1=tk.Frame(root, bg='grey' ,borderwidth=5, relief='sunken')
f1.pack(side="left", fill="y")
l=tk.Label(f1,text=' Its sidebar', fg="red")
l.pack(pady=150)

f2=tk.Frame(root,borderwidth=7, bg='grey')
f2.pack(side='top', fill='x')
l=tk.Label(f2,text="welcome to topbar", fg='red', font="helvetica 20 bold")
l.pack(padx=130)


b1=tk.Button(root,text="click me", command=printName)
b1.pack(pady=20)



root.mainloop()