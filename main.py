import tkinter as tk
from pages import StartPage, RegisterPage, LoginPage, HomePage, SearchPage, BorrowedBooksPage, AccountPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Library')
        self.geometry('680x480')

        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        self.frames = {}

        for F in (StartPage, RegisterPage, LoginPage, HomePage, SearchPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame  # Use class name as string for key
            frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("StartPage")  # Reference frames using class names as strings

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def add_menu(self, frame):
        menu_bar = tk.Menu(frame)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=file_menu)
        file_menu.add_command(label="Start Page", command=lambda: self.show_frame(StartPage))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)


if __name__ == "__main__":
    app = App()
    app.mainloop()
