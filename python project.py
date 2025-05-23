import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Book:
    def __init__(self, name, author_name, book_id, shelf, status):
        self.name = name
        self.author_name = author_name
        self.book_id = book_id
        self.shelf = shelf
        self.status = status

class Library:
    
    def __init__(self):
        self.book_list = []

    def add_book(self, book):
        self.book_list.append(book)

    def get_books_sorted_by_author(self):
        return sorted(self.book_list, key=lambda x: x.author_name.lower())

    def get_books_sorted_by_shelf(self):
        return sorted(self.book_list, key=lambda x: x.shelf)

    def search_book(self, name):
        for book in self.book_list:
            if book.name.lower() == name.lower():
                return book
        return None

    def edit_book(self, name, new_shelf, new_status):
        book = self.search_book(name)
        if book:
            book.shelf = new_shelf
            book.status = new_status
            return True
        return False

    def remove_book(self, name):
        book = self.search_book(name)
        if book:
            self.book_list.remove(book)
            return True
        return False

    def save_books(self):
        with open("books.txt", "w") as file:
            for book in self.book_list:
                file.write(f"{book.name},{book.author_name},{book.book_id},{book.shelf},{book.status}\n")

    def load_books(self):
        if os.path.exists("books.txt"):
            with open("books.txt", "r") as file:
                for line in file:
                    name, author_name, book_id, shelf, status = line.strip().split(",")
                    book = Book(name, author_name, book_id, int(shelf), status)
                    self.book_list.append(book)

class LibraryGUI:
    def __init__(self, root):
        self.library = Library()
        self.library.load_books()
        self.root = root
        self.root.title("🌟 Library Management System 🌟")
        self.root.geometry("800x600")
        self.root.configure(bg="#1f2937")  # dark background

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', font=('Segoe UI', 11), padding=6)
        self.style.configure('TLabel', background="#1f2937", foreground="white", font=('Segoe UI', 12))
        self.style.configure('Treeview', background="#f9fafb", foreground="black", fieldbackground="#f9fafb", font=('Segoe UI', 11))
        self.style.map('Treeview', background=[('selected', '#2563eb')], foreground=[('selected', 'white')])

        self.create_widgets()

    def create_widgets(self):
        frame = tk.Frame(self.root, bg="#1f2937")
        frame.pack(pady=20)

        tk.Label(frame, text="Library Management", font=('Segoe UI', 24, 'bold'), fg="#3b82f6", bg="#1f2937").grid(row=0, column=0, columnspan=4, pady=10)

        ttk.Button(frame, text="Add Book", command=self.add_book).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(frame, text="Display Books (Author)", command=lambda: self.display_books(sort_by='author')).grid(row=1, column=1, padx=10, pady=10)
        ttk.Button(frame, text="Display Books (Shelf)", command=lambda: self.display_books(sort_by='shelf')).grid(row=1, column=2, padx=10, pady=10)
        ttk.Button(frame, text="Search Book", command=self.search_book).grid(row=1, column=3, padx=10, pady=10)

        ttk.Button(frame, text="Edit Book", command=self.edit_book).grid(row=2, column=0, padx=10, pady=10)
        ttk.Button(frame, text="Remove Book", command=self.remove_book).grid(row=2, column=1, padx=10, pady=10)
        ttk.Button(frame, text="Check Status", command=self.check_status).grid(row=2, column=2, padx=10, pady=10)
        ttk.Button(frame, text="Exit", command=self.exit_app).grid(row=2, column=3, padx=10, pady=10)

        self.tree = ttk.Treeview(self.root, columns=("Name", "Author", "ID", "Shelf", "Status"), show="headings", height=15)
        for col in ("Name", "Author", "ID", "Shelf", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140, anchor='center')

        self.tree.pack(pady=10)

    def clear_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

    def display_books(self, sort_by):
        self.clear_tree()
        if sort_by == 'author':
            books = self.library.get_books_sorted_by_author()
        else:
            books = self.library.get_books_sorted_by_shelf()
        for book in books:
            self.tree.insert("", "end", values=(book.name, book.author_name, book.book_id, book.shelf, book.status))

    def add_book(self):
        name = simpledialog.askstring("Input", "Enter the name of the book:", parent=self.root)
        if not name:
            return
        author = simpledialog.askstring("Input", "Enter the author of the book:", parent=self.root)
        if not author:
            return
        book_id = simpledialog.askstring("Input", "Enter the book ID:", parent=self.root)
        if not book_id:
            return
        try:
            shelf = simpledialog.askinteger("Input", "Enter the shelf number:", parent=self.root, minvalue=1)
        except:
            messagebox.showerror("Error", "Invalid shelf number!")
            return
        if shelf is None:
            return
        status = simpledialog.askstring("Input", "Enter the status of the book:", parent=self.root)
        if not status:
            return
        book = Book(name, author, book_id, shelf, status)
        self.library.add_book(book)
        messagebox.showinfo("Success", "Book added successfully!")
        self.display_books('author')

    def search_book(self):
        name = simpledialog.askstring("Search", "Enter the name of the book:", parent=self.root)
        if not name:
            return
        book = self.library.search_book(name)
        if book:
            messagebox.showinfo("Book Found",
                                f"Name: {book.name}\nAuthor: {book.author_name}\nID: {book.book_id}\nShelf: {book.shelf}\nStatus: {book.status}")
        else:
            messagebox.showwarning("Not Found", "Book not found!")

    def edit_book(self):
        name = simpledialog.askstring("Edit", "Enter the name of the book to edit:", parent=self.root)
        if not name:
            return
        book = self.library.search_book(name)
        if not book:
            messagebox.showwarning("Not Found", "Book not found!")
            return
        new_shelf = simpledialog.askinteger("Edit", "Enter new shelf number:", parent=self.root, minvalue=1)
        if new_shelf is None:
            return
        new_status = simpledialog.askstring("Edit", "Enter new status:", parent=self.root)
        if not new_status:
            return
        self.library.edit_book(name, new_shelf, new_status)
        messagebox.showinfo("Success", "Book updated successfully!")
        self.display_books('author')

    def remove_book(self):
        name = simpledialog.askstring("Remove", "Enter the name of the book to remove:", parent=self.root)
        if not name:
            return
        if self.library.remove_book(name):
            messagebox.showinfo("Success", "Book removed successfully!")
            self.display_books('author')
        else:
            messagebox.showwarning("Not Found", "Book not found!")

    def check_status(self):
        name = simpledialog.askstring("Status", "Enter the name of the book:", parent=self.root)
        if not name:
            return
        book = self.library.search_book(name)
        if book:
            messagebox.showinfo("Status", f"Status of '{book.name}' is: {book.status}")
        else:
            messagebox.showwarning("Not Found", "Book not found!")

    def exit_app(self):
        self.library.save_books()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryGUI(root)
    root.mainloop()
