import json
import os

data_file = "library.txt"

def load_lib():
    if os.path.exists(data_file):
        with open(data_file, 'r') as file:
            return json.load(file)
    return []

def save_lib(library):
    with open(data_file, 'w') as file:
        json.dump(library, file)

def add_book(library):
    title = input('Enter the title of the book: ')
    author = input("Enter the Author's name: ")
    year = input('Enter the year of the book: ')
    genre = input("Enter the genre of the book: ")
    read = input('Have You read the book? (Yes/No): ').lower() == 'yes'

    new_book = {
        'title': title,
        'author': author,
        'year' : year,
        'genre': genre,
        'read': read
    }

    library.append(new_book)
    save_lib(library)
    print(f'Book {title} added successfully!')

def remove_book(library):
        title = input('Enter the title of the book to remove from the library: ')
        initial_length = len(library)
        library = [book for book in library if book['title'].lower() != title]
        if len(library) < initial_length:
            save_lib(library)
            print(f'Book {title} removed successfully!')
        else:
            print(f'Book {title} not found in the library.')

def search_lib(library):
    print("Search by:  ")
    print("1. Title  ")
    print("2. Author  ")
    choice = input("Enter your choice: ")

    if choice == '1':
        search_by = 'title'
    elif choice == '2':
        search_by = 'author'
    else:
        print("Invalid choice.")
        return

    search_term = input(f"Enter the {search_by}: ").lower()

    results = []
    for book in library:
        if search_term in book[search_by].lower():
            results.append(book)

    if results:
        print("Matching Books:")
        for i, book in enumerate(results, 1):
            status = "Read" if book['read'] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        print("No matching books found.")

def display_all_books(library):
    if library:
        for i, book in enumerate(library, 1):
            status = 'Read' if book['read'] else "Unread"
            print(f"{i}. {book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
    else:
        print("The library is empty.")

def display_stats(library):
    total_books =  len(library)
    read_books = len([book for book in library if book['read']])
    percentage_read = (read_books / total_books) * 100 if total_books > 0 else 0

    print(f"Total books: {total_books}")
    print(f"Percentage read: {percentage_read:.2f}%")

def main():
    library = load_lib()
    while True:
        print("Welcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book")
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

        choice = input("Enter Your choice: ")
        if choice == '1':
            add_book(library)
        elif choice == '2':
            remove_book(library)
        elif choice == '3':
            search_lib(library)
        elif choice == '4':
            display_all_books(library)
        elif choice == '5':
            display_stats(library)
        elif choice == '6':
            print("Library saved to file. GoodBye!")
            break
        else:
            print("Invalid choice. Please try again!")

if __name__ == '__main__':
    main()
        