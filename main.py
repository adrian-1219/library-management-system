import tkinter as tk
from pages import StartPage, RegisterPage, LoginPage, HomePage, SearchPage, BorrowedBooksPage, AccountPage, \
    BookDetailsPage

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Library Management System')
        self.geometry('1280x680')

        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        self.username = None
        self.frames = {}

        # # set a single font to be used throughout the app
        # self.title_font = tkfont.Font(
        #     family='Helvetica', size=18, weight="bold", slant="italic")

        # Create all the pages, this needs to be updated
        # for each other custom Frame class you make, you could add it to this tuple
        for F in (StartPage, RegisterPage, LoginPage, HomePage, SearchPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame  # Use class name as string for key
            frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        self.show_frame("HomePage")

    def show_frame(self, cont):
        """Show a frame for the given page name"""
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

    # a function that will show the details of a book according to the book_id
    def show_book(self, cont, book):
        frame = BookDetailsPage(parent=self.container, controller=self, book=book)
        self.frames[cont] = frame
        frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        frame.tkraise()

    # this needs to be ran after self.controller.username is set, otherwise it doesn't retrieve the username properly
    def show_borrow_history(self, cont):
        frame = BorrowedBooksPage(parent=self.container, controller=self)
        self.frames[cont] = frame
        frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()
