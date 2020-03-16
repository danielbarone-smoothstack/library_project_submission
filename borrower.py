from user import User
import constants
from procedures import (
    card_number_exists,
    borrower_return_book,
    checkout_book,
    duplicate_loan_check
)
'''
NOTE: Checking out a duplicate results in sql error and program termincation
'''
class Borrower(User):

    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.user_type = constants.bcolor.get_color('header', 'Borrower')

    def checkout_book(self, cardNo):

        self.print_submenu('Pick the branch you want to check out from:')
        branch_info = self.get_branch_selection() # ID, Name, Address

        if isinstance(branch_info, bool):
            if branch_info == True:
                return True
            else:
                return False

        self.print_submenu('Pick the book you want to check out')
        book_info = self.get_book_selection(branch_info[0], None) # ID, Name

        if isinstance(book_info, bool):
            if book_info == True:
                print('returning true from borrower checkout section')
                return True
            elif book_info == False:
                print('Returning falsefrom borrower checkout section')
                return False

        if duplicate_loan_check(self.cursor, self.connection, book_info[0], branch_info[0], cardNo):
            print('You already borrowed that book, from that branch!')
            return True
        else :
            checkout_book(self.cursor, self.connection, book_info[0], branch_info[0], cardNo)
            return True

    def return_book(self, cardNo):
        self.print_submenu('Pick the branch you want to return a book to:')
        branch_info = self.get_branch_selection() # ID, Name, Address

        if isinstance(branch_info, bool):
            if branch_info == True:
                return True
            else:
                return False

        self.print_submenu('Pick the book you want to return')
        book_info = self.get_book_selection(branch_info[0], cardNo) # ID, Name

        if isinstance(book_info, bool):
            if book_info == True:
                return True
            elif book_info == False:
                return False

        successful_return = borrower_return_book(self.cursor, self.connection, book_info[0], branch_info[0], cardNo)
        if not successful_return:
            print('couldnt return book')
        return successful_return

    def check_card_valid(self):
        cardNumberValid = False

        while not cardNumberValid:
            cardNo = input(constants.CARD_NUMBER_PROMPT)

            if cardNo.isdigit():
                cardNo = int(cardNo)
                if card_number_exists(self.cursor, cardNo):
                    cardNumberValid = True
                    return cardNo
                else:
                    print(constants.TRY_AGAIN)
            elif cardNo == 'quit':
                return False
            else:
                print(constants.TRY_AGAIN)

    def driver(self):

        self.print_menu(self.user_type)

        card_number = self.check_card_valid()

        if not card_number:
            return False

        BORROWER_OPTIONS = {
            1: lambda: self.checkout_book(card_number),
            2: lambda: self.return_book(card_number),
        }

        return self.prompt_options(
            constants.MAIN_BORROWER_OPTIONS,
            BORROWER_OPTIONS
        )

