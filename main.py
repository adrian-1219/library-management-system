import tkinter as tk
from tkinter.font import Font

from pages import StartPage, RegisterPage, LoginPage, HomePage, SearchPage, BorrowedBooksPage, AccountPage, \
    BookDetailsPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Library Management System')
        window_width = 1280
        window_height = 680
        # center the program window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        self.geometry("%dx%d+%d+%d" % (window_width, window_height, x, y))
        self.resizable(False, False)
        # self.set_default_font()
        self.container = tk.Frame(self)
        self.container.pack(expand=True, fill="both")
        self.current_frame = None
        self.username = None
        self.frames = {}
        self.db_font = Font(family="Times New Roman", size=16)
        self.bd_FONT = Font(family="Times New Roman", size=16, weight="bold")

        # set a single font to be used throughout the app
        # self.title_font = tkfont.Font(
        #     family='Helvetica', size=18, weight="bold", slant="italic")

        # Create all the pages, this needs to be updated
        # for each other custom Frame class you make, you could add it to this tuple
        for F in (StartPage, RegisterPage, LoginPage, HomePage, SearchPage, AccountPage, BorrowedBooksPage, BookDetailsPage):
            frame = F(parent=self.container, controller=self)
            self.frames[F.__name__] = frame  # Use class name as string for key
            frame.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)

        # self.toolbar.save_default_font()

        # User must login for borrow history to work
        self.show_frame("StartPage")

    # not working
    # def set_default_font(self):
    #     print("setting default font")
    #     default_font = tkfont.Font(family='Times New Roman', size=12)
    #     self.option_add("*Font", default_font)

    def show_frame(self, cont):
        """Show a frame for the given page name"""
        frame = self.frames[cont]
        # if cont == 'AcocuntPage' and username is not None:
        #     frame.set_username(username)
        frame.tkraise()
        self.current_frame = cont

    def add_menu(self, frame):
        menu_bar = tk.Menu(frame)
        self.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Help", menu=file_menu)
        # file_menu.add_command(label="Start Page", command=lambda: self.show_frame(StartPage))
        # file_menu.add_separator()
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

    def walk_widgets(self, container=None):
        if container is None:
            container = self
        # Check if the widget has the 'winfo_children' method
        if hasattr(container, 'winfo_children'):
            for widget in container.winfo_children():
                yield widget
                # Recursively yield from child widgets
                yield from self.walk_widgets(widget)


if __name__ == "__main__":
    app = App()
    app.mainloop()

