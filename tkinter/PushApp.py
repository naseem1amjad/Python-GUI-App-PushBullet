import tkinter as tk
import time

class MessageApp:

    def __init__(self, master):
        self.master = master
        self.master.geometry("320x400")
        self.master.title("Message App")

        self.token_number = None
        self.time_interval = None
        self.message = None
        self.message_text = tk.StringVar()
        self.message_text.set("Ready")
        self.loop_started = False

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.master, text="Select a message file:").pack(pady=10)

        self.message_button = tk.Button(self.master, text="Browse", command=self.browse_message_file)
        self.message_button.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_loop, state=tk.DISABLED)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.master, text="Stop", command=self.stop_loop, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.status_label = tk.Label(self.master, textvariable=self.message_text)
        self.status_label.pack(side=tk.BOTTOM, pady=20)

        self.message_label = tk.Label(self.master, text="", wraplength=300)
        self.message_label.pack(pady=10)

    def browse_message_file(self):
        from tkinter.filedialog import askopenfilename
        self.message = askopenfilename()
        if self.message:
            self.message_label.config(text="Selected message file: " + self.message)
            self.start_button.config(state=tk.NORMAL)
        else:
            self.message_label.config(text="")
            self.start_button.config(state=tk.DISABLED)

    def start_loop(self):
        self.loop_started = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.message_text.set("Loop Started")
        self.token_number = 0
        self.time_interval = 5
        self.loop()

    def stop_loop(self):
        self.loop_started = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.message_text.set("Loop Stopped")

    def loop(self):
        if self.loop_started:
            self.token_number += 1
            with open(self.message, "r") as file:
                message = file.read()
            self.message_label.config(text=message)
            print(message)
            self.master.after(self.time_interval * 1000, self.loop)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MessageApp(root)
    app.run()
