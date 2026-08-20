from tkinter import tk
from tkinter import ttk
root=tk.Tk()
l1=tk.Label(root,text="Classic Theme").pack()
ttk.Label(root,text="Themed Tk").pack()
# windows=tk.Tk()
# windows.title("Dashboard")
root.title("Tkinter Demo")


# root.geometry("600x400+50+50")
# # root.resizable(False,False)
# root.minsize(400,400)
# root.maxsize(700,700)
# # windows.attributes("-topmost",True)
# # root.lower(True)

# # root.attributes("-alpha",0.8)


# msg=tk.Label(root, text="Hello word")
# msg.pack()
root.mainloop()