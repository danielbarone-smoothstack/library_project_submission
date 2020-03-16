class bcolors:
    def __init__(self):
        self.HEADER = '\033[95m'
        self.OKBLUE = '\033[94m'
        self.OKGREEN = '\033[92m'
        self.WARNING = '\033[93m'
        self.FAIL = '\033[91m'
        self.ENDC = '\033[0m'
        self.BOLD = '\033[1m'
        self.UNDERLINE = '\033[4m'

        self.colors = {
            'blue': self.OKBLUE,
            'green': self.OKGREEN,
            'red': self.FAIL,
            'header': self.HEADER
        }
    
    def get_color(self, color, text):
        return self.colors[color] + text + self.ENDC

bcolor = bcolors()
INCORRECT_INPUT = bcolor.FAIL + '\nInvalid selection. Try again or type \'quit\' if you wish to quit.\n' + bcolor.ENDC
QUIT_MESSAGE = bcolor.get_color('green', '\nGood Bye.\n')
PREVIOUS_MENU = bcolor.get_color('blue', 'Quit to previous menu')
MAKE_SELECTION = 'Please make a selection: '
LINE_BREAK = '---------------------------------------'
MENU_LINE_BREAK = '======================================='

# driver.py
WELCOME_MESSAGE = bcolor.get_color('header', 'Welcome to the GCIT Library Management\nSystem. Which category of user are you?')
USER_TYPES = '1) ' + bcolor.OKBLUE + 'Librarian\n' + bcolor.ENDC + '2) ' + bcolor.OKBLUE + 'Administrator\n' + bcolor.ENDC + '3) ' + bcolor.OKBLUE + 'Borrower' + bcolor.ENDC

# librarian.py
ENTER_BRANCH = bcolor.get_color('blue', 'Enter Branch you manage')
LIB1_OPTIONS = [ENTER_BRANCH]
UPDATE_LIBRARY = bcolor.get_color('blue', 'Update the details of the Library')
ADD_COPIES = bcolor.get_color('blue', 'Add Copies of a Book to the Branch')
LIB3_OPTIONS = [UPDATE_LIBRARY, ADD_COPIES]

# borrower.py
CARD_NUMBER_PROMPT = bcolor.get_color('blue', 'Enter your card number: ')
TRY_AGAIN = bcolor.get_color('red', '\nPlease try a different number.\n')

# BORR1
CHECKOUT = bcolor.get_color('blue', 'Check out a book')
RETURN = bcolor.get_color('blue', 'Return a book')
MAIN_BORROWER_OPTIONS = [CHECKOUT, RETURN]
CHECKOUT_BRANCH = bcolor.get_color('blue', 'Pick the branch you want to check out from:\n')
CHECKOUT_BOOK = bcolor.get_color('blue', 'Pick the book you want to check out:\n')
RETURN_BRANCH = bcolor.get_color('blue', 'Pick the branch you want to return a book to:\n')
RETURN_BOOK = bcolor.get_color('blue', 'Pick the book you want to return:\n')


# administrator.py
## driver function
AUD_BOOK_AND_AUTHOR = bcolor.get_color('blue', 'Add/Update/Delete Book and Author')
AUD_PUBLISHERS = bcolor.get_color('blue', 'Add/Update/Delete Publishers')
AUD_LIBRARY_BRANCHES = bcolor.get_color('blue', 'Add/Update/Delete Library Branches')
AUD_BORROWERS = bcolor.get_color('blue', 'Add/Update/Delete Borrowers')
OVERRIDE_DUEDATE = bcolor.get_color('blue', 'Override Due Date for a Book Loan')
MAIN_ADMIN_OPTIONS = [
    AUD_BOOK_AND_AUTHOR, 
    AUD_PUBLISHERS, 
    AUD_LIBRARY_BRANCHES, 
    AUD_BORROWERS, 
    OVERRIDE_DUEDATE, 
]
## aud book and author
ADD_BOOK_AND_AUTHOR = bcolor.get_color('blue', 'Add Book and Author')
UPDATE_BOOK_AND_AUTHOR = bcolor.get_color('blue', 'Update Book and Author')
DELETE_BOOK_AND_AUTHOR = bcolor.get_color('blue', 'Delete Book and Author')
ADMIN_BOOK_AND_AUTHOR_OPTIONS = [
    ADD_BOOK_AND_AUTHOR,
    UPDATE_BOOK_AND_AUTHOR,
    DELETE_BOOK_AND_AUTHOR
]
ADD_MORE_AUTHORS = bcolor.get_color('header', 'Add another author?\n') + '1) ' + bcolor.get_color('blue', 'Yes\n') + '2) ' + bcolor.get_color('blue', 'No')
## aud branches
NOT_APPLICABLE = 'N/A'
ADD_BRANCH = bcolor.get_color('blue', 'Add a branch')
UPDATE_BRANCH = bcolor.get_color('blue', 'Update a branch')
DELETE_FROM_BRANCH = bcolor.get_color('blue', 'Delete a branch')
ADMIN_BRANCH_OPTIONS = [
    ADD_BRANCH,
    UPDATE_BRANCH,
    DELETE_FROM_BRANCH
]
# aud publishers
ADD_PUBLISHER = bcolor.get_color('blue', 'Add a publisher')
UPDATE_PUBLISHER = bcolor.get_color('blue', 'Update a publisher')
DELETE_PUBLISHER = bcolor.get_color('blue', 'Delete a publisher')
PUBLISHER_OPTIONS = [ADD_PUBLISHER, UPDATE_PUBLISHER, DELETE_PUBLISHER]

# aud borrowers
ADD_BORROWER = bcolor.get_color('blue', 'Add a Borrower')
UPDATE_BORROWER = bcolor.get_color('blue', 'Update a Borrower')
DELETE_BORROWER = bcolor.get_color('blue', 'Delete a Borrower')
AUD_BORROWER_OPTIONS = [ADD_BORROWER, UPDATE_BORROWER, DELETE_BORROWER]