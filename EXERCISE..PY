import sqlite3

# Function to create the database and tables
def create_database():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    # Create Books table
    c.execute('''CREATE TABLE IF NOT EXISTS Books
                 (BookID INTEGER PRIMARY KEY,
                 Title TEXT,
                 Author TEXT,
                 ISBN TEXT,
                 Status TEXT)''')

    # Create Users table
    c.execute('''CREATE TABLE IF NOT EXISTS Users
                 (UserID INTEGER PRIMARY KEY,
                 Name TEXT,
                 Email TEXT)''')

    # Create Reservations table
    c.execute('''CREATE TABLE IF NOT EXISTS Reservations
                 (ReservationID INTEGER PRIMARY KEY,
                 BookID INTEGER,
                 UserID INTEGER,
                 ReservationDate TEXT,
                 FOREIGN KEY (BookID) REFERENCES Books(BookID),
                 FOREIGN KEY (UserID) REFERENCES Users(UserID))''')

    conn.commit()
    conn.close()

# Function to add a new book to the database
def add_book():
    title = input("Enter the title of the book: ")
    author = input("Enter the author of the book: ")
    isbn = input("Enter the ISBN of the book: ")
    status = input("Enter the status of the book: ")

    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("INSERT INTO Books (Title, Author, ISBN, Status) VALUES (?, ?, ?, ?)", (title, author, isbn, status))

    conn.commit()
    conn.close()

    print("Book added successfully!")

# Function to find a book's details based on BookID
def find_book_details(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if book is None:
        print("Book not found!")
        return

    c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
    reservation = c.fetchone()

    if reservation is None:
        print("Book is not reserved.")
    else:
        user_id = reservation[2]
        c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
        user = c.fetchone()
        print("Reserved by:", user[1], "(UserID:", user[0], ")")

    print("Book details:")
    print("BookID:", book[0])
    print("Title:", book[1])
    print("Author:", book[2])
    print("ISBN:", book[3])
    print("Status:", book[4])

    conn.close()

# Function to find a book's reservation status based on BookID, Title, UserID, or ReservationID
def find_reservation_status(text):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    if text.startswith('LB'):
        c.execute("SELECT * FROM Books WHERE BookID=?", (text,))
        book = c.fetchone()

        if book is None:
            print("Book not found!")
        else:
            print("Reservation status:", book[4])
    elif text.startswith('LU'):
        c.execute("SELECT * FROM Users WHERE UserID=?", (text,))
        user = c.fetchone()

        if user is None:
            print("User not found!")
        else:
            c.execute("SELECT * FROM Reservations WHERE UserID=?", (user[0],))
            reservations = c.fetchall()

            if len(reservations) == 0:
                print("User has no reservations.")
            else:
                print("User's reservations:")
                for reservation in reservations:
                    book_id = reservation[1]
                    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
                    book = c.fetchone()
                    print("Book:", book[1], "(BookID:", book[0], ")")
    elif text.startswith('LR'):
        c.execute("SELECT * FROM Reservations WHERE ReservationID=?", (text,))
        reservation = c.fetchone()

        if reservation is None:
            print("Reservation not found!")
        else:
            book_id = reservation[1]
            user_id = reservation[2]
            c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
            book = c.fetchone()
            c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
            user = c.fetchone()
            print("Book:", book[1], "(BookID:", book[0], ")")
            print("Reserved by:", user[1], "(UserID:", user[0], ")")
    else:
        c.execute("SELECT * FROM Books WHERE Title=?", (text,))
        books = c.fetchall()

        if len(books) == 0:
            print("Book not found!")
        else:
            print("Books found:")
            for book in books:
                print("Book:", book[1], "(BookID:", book[0], ")")
                c.execute("SELECT * FROM Reservations WHERE BookID=?", (book[0],))
                reservation = c.fetchone()

                if reservation is None:
                    print("Reservation status: Not reserved")
                else:
                    user_id = reservation[2]
                    c.execute("SELECT * FROM Users WHERE UserID=?", (user_id,))
                    user = c.fetchone()
                    print("Reserved by:", user[1], "(UserID:", user[0], ")")

    conn.close()

# Function to find all books in the database
def find_all_books():
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Books")
    books = c.fetchall()

    if len(books) == 0:
        print("No books found!")
    else:
        print("All books in the database:")
        for book in books:
            print("BookID:", book[0])
            print("Title:", book[1])
            print("Author:", book[2])
            print("ISBN:", book[3])
            print("Status:", book[4])
            print("")

    conn.close()

# Function to modify/update book details based on BookID
def update_book_details(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if book is None:
        print("Book not found!")
        return

    new_title = input("Enter the new title (leave blank to keep the same): ")
    new_author = input("Enter the new author (leave blank to keep the same): ")
    new_isbn = input("Enter the new ISBN (leave blank to keep the same): ")
    new_status = input("Enter the new status (leave blank to keep the same): ")

    if new_title:
        c.execute("UPDATE Books SET Title=? WHERE BookID=?", (new_title, book_id))
    if new_author:
        c.execute("UPDATE Books SET Author=? WHERE BookID=?", (new_author, book_id))
    if new_isbn:
        c.execute("UPDATE Books SET ISBN=? WHERE BookID=?", (new_isbn, book_id))
    if new_status:
        c.execute("UPDATE Books SET Status=? WHERE BookID=?", (new_status, book_id))

    conn.commit()
    conn.close()

    print("Book details updated successfully!")

# Function to delete a book based on its BookID
def delete_book(book_id):
    conn = sqlite3.connect('library.db')
    c = conn.cursor()

    c.execute("SELECT * FROM Books WHERE BookID=?", (book_id,))
    book = c.fetchone()

    if book is None:
        print("Book not found!")
        return

    c.execute("SELECT * FROM Reservations WHERE BookID=?", (book_id,))
    reservation = c.fetchone()

    if reservation is not None:
        c.execute("DELETE FROM Reservations WHERE BookID=?", (book_id,))

    c.execute("DELETE FROM Books WHERE BookID=?", (book_id,))

    conn.commit()
    conn.close()

    print("Book deleted successfully!")

# Main program loop
def library_management_system():
    create_database()

    while True:
        print("\n--- Library Management System Menu ---")
        print("1. Add a new book")
        print("2. Find a book's details based on BookID")
        print("3. Find a book's reservation status")
        print("4. Find all books")
        print("5. Modify/update book details")
        print("6. Delete a book")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            book_id = input("Enter the BookID: ")
            find_book_details(book_id)
        elif choice == '3':
            text = input("Enter the BookID, Title, UserID, or ReservationID: ")
            find_reservation_status(text)
        elif choice == '4':
            find_all_books()
        elif choice == '5':
            book_id = input("Enter the BookID: ")
            update_book_details(book_id)
        elif choice == '6':
            book_id = input("Enter the BookID: ")
            delete_book(book_id)
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

# Run the library management system
library_management_system()