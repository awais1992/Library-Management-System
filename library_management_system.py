# ------------------------------------------------------------
# Library Management System (Final Project)
# Author: Owais Khan
# Description:
# A complete Library Management System in Python that supports
# adding, removing, viewing, borrowing, and returning books.
# Demonstrates Object-Oriented Programming, File Handling,
# and Exception Handling.
# ------------------------------------------------------------

# --- Class Definitions ---

class Book:
    """Represents a single book in the library."""
    def __init__(self, book_id, title, author, status="available"):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.status = status

    def __str__(self):
        """Readable string format for displaying book info."""
        return f"{self.book_id}: {self.title} by {self.author} - Status: {self.status}"


class Member:
    """Represents a library member who can borrow books."""
    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def __str__(self):
        """Readable string format for displaying member info."""
        return f"{self.name} (ID: {self.member_id})"


class Library:
    """Main class that manages all books and members."""
    def __init__(self):
        self.books = []
        self.members = []

    # ----------------------------------------------------
    # Book Management Functions
    # ----------------------------------------------------
    def add_book(self, book):
        """Add a new book to the library."""
        self.books.append(book)
        print(f"Book '{book.title}' added to the library.")

    def view_books(self):
        """Display all books currently in the library."""
        if not self.books:
            print("No books available in the library.")
        else:
            print("\nLibrary Books:")
            for book in self.books:
                print(f"  {book}")

    def remove_book(self, book_id):
        """Remove a book from the library by its ID."""
        for book in self.books:
            if book.book_id == book_id:
                self.books.remove(book)
                print(f"Book '{book.title}' removed successfully.")
                return
        print("Book not found.")

    # ----------------------------------------------------
    # Member Management
    # ----------------------------------------------------
    def find_member_by_id(self, member_id):
        """Find and return a member object by ID."""
        for member in self.members:
            if member.member_id == member_id:
                return member
        return None

    # ----------------------------------------------------
    # Borrowing and Returning Books
    # ----------------------------------------------------
    def borrow_book(self, book_id, member):
        """Allow a member to borrow a book if available."""
        for book in self.books:
            if book.book_id == book_id:
                if book.status == "available":
                    book.status = "borrowed"
                    member.borrowed_books.append(book)
                    print(f"{member.name} borrowed '{book.title}'.")
                    return
                else:
                    print("This book is already borrowed.")
                    return
        print("Book not found.")

    def return_book(self, book_id, member):
        """Allow a member to return a borrowed book."""
        # Find the book in the library
        for book in self.books:
            if book.book_id == book_id:
                # Check if this member has borrowed a book with the same ID
                for borrowed in member.borrowed_books:
                    if borrowed.book_id == book_id:
                        book.status = "available"
                        member.borrowed_books.remove(borrowed)
                    print(f"{member.name} returned '{book.title}'.")
                    return
                else:
                    print("This member did not borrow this book.")
                    return
        print("Book not found.")

    # ----------------------------------------------------
    # File Handling
    # ----------------------------------------------------
    def save_data(self, filename="library_data.txt"):
        """Save all books to a text file."""
        try:
            with open(filename, "w") as file:
                for book in self.books:
                    file.write(f"{book.book_id},{book.title},{book.author},{book.status}\n")
            print("Library data saved successfully.")
        except IOError:
            print("Error: Unable to save library data.")

    def load_data(self, filename="library_data.txt"):
        """Load all books from a text file (if it exists)."""
        try:
            with open(filename, "r") as file:
                for line in file:
                    book_id, title, author, status = line.strip().split(",")
                    self.books.append(Book(book_id, title, author, status))
            print("Library data loaded successfully.")
        except FileNotFoundError:
            print("Data file not found. Starting with an empty library.")


# ------------------------------------------------------------
# Menu Interface
# ------------------------------------------------------------

def main():
    """Main menu interface for user interaction."""
    library = Library()
    library.load_data()  # Load existing books (if available)

    while True:
        print("\n========= LIBRARY MENU =========")
        print("1. View Books")
        print("2. Add Book")
        print("3. Remove Book")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. Exit")
        print("================================")

        try:
            choice = int(input("Enter your choice (1–6): "))

            if choice == 1:
                library.view_books()

            elif choice == 2:
                book_id = input("Enter book ID: ")
                title = input("Enter book title: ")
                author = input("Enter book author: ")
                book = Book(book_id, title, author)
                library.add_book(book)

            elif choice == 3:
                book_id = input("Enter book ID to remove: ")
                library.remove_book(book_id)

            elif choice == 4:
                member_name = input("Enter member name: ")
                member_id = input("Enter member ID: ")

                # Check if member already exists
                member = library.find_member_by_id(member_id)
                if not member:
                    member = Member(member_name, member_id)
                    library.members.append(member)

                book_id = input("Enter book ID to borrow: ")
                library.borrow_book(book_id, member)

            elif choice == 5:
                member_id = input("Enter member ID: ")

                # Find existing member
                member = library.find_member_by_id(member_id)
                if not member:
                    print("Member not found in records.")
                else:
                    book_id = input("Enter book ID to return: ")
                    library.return_book(book_id, member)

            elif choice == 6:
                library.save_data()
                print("Goodbye! Have a great day at the library.")
                break

            else:
                print("Invalid choice. Please select between 1 and 6.")

        except ValueError:
            print("Please enter a valid number (1-6).")


# Run the program only if this file is executed directly
if __name__ == "__main__":
    main()
