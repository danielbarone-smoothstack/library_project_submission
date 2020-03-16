## Team RoughQueue
Members: Cole Trumbo, Daniel Barone, Kevin Lai, Rory Burke

# Library Project

## Running Program
* Requirements: Python 3+, mysql-connector-python
* Navigate to project directory
```
python driver.py
```

## driver.py
* Main driver of the program
* Runs on while loop prompting menu options
* When the selection is made, the corresponding class' driver function is called

    - main()
    - entryPrompt()

## user.py
* Polymorphism
* Admin, Librarian, and Borrower are subclasses

    - __init__(cursor, connection)
    - get_selection()
    - get_book_selection()
    - get_branch_selection()
    - print_menu()
    - print_submenu()
    - prompt_options()

## librarian.py
* Update Branch Details
* Add Copies to Book

    - driver()
    - LIB2()
    - LIB3()
    - add_copies()
    - update_lib_details()

## borrower.py
* Checkout Book
* Return Book 

    - driver()
    - check_card_valid()
    - checkout_book()
    - return_book()

## administrator.py
* AUD book and author, publishers, library branches, borrowers, override due date


## procedures.py
* Connection

## library_objects.py
    - Book
    - BookLoan
    - Branch
    - Publisher
