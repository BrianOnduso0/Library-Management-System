from utils import *

# Main program
def main():
    while True:
        print("\nChoose an action:")
        print("1. List Members (Admin Only)")
        print("2. Add Member (Admin Only)")
        print("3. Remove Member (Admin Only)")
        print("4. Add Book (Admin Only)")
        print("5. Remove Book (Admin Only)")
        print("6. List Books")
        print("7. Borrow Book")
        print("8. Return Book")
        print("9. View Borrowed Books")
        print("10. Exit")
        
        choice = input("Enter your choice: ")

        if choice == '1':
            list_members()
        elif choice == '2':
            name = input("Enter member name: ")
            add_member(name)
        elif choice == '3':
            name = input("Enter member name to remove: ")
            remove_member(name)
        elif choice == '4':
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            quantity = int(input("Enter quantity: "))
            add_book(title, author, quantity)
        elif choice == '5':
            title = input("Enter book title to remove: ")
            remove_book(title)
        elif choice == '6':
            list_books()
        elif choice == '7':
            member_name = input("Enter member name: ")
            book_title = input("Enter book title to borrow: ")
            borrow_book(member_name, book_title, 1)
        elif choice == '8':
            member_name = input("Enter member name: ")
            book_title = input("Enter book title to return: ")
            return_book(member_name, book_title, 1)
        elif choice == '9':
            list_borrowed_books()
        elif choice == '10':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")


if __name__ == "__main__":
    main()
