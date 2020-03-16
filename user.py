import constants
from procedures import (
    get_branches,
    get_books_by_branch_id,
    get_num_copies,
    get_books_due,
    get_num_books_on_loan,
    get_authors_by_book
)
from library_objects import Branch

class User:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def get_selection(self):
        print(constants.LINE_BREAK)
        return input(constants.MAKE_SELECTION)

    def get_book_selection(self, branch, cardNo=None, fromUpdateBook=False): # num copies > 0
        book_dictionary = {}

        # Checking out a book
        if cardNo == None:
            book_dictionary = get_books_by_branch_id(self.cursor, branch)
        # returning a book
        else:
            book_dictionary = get_books_due(self.cursor, cardNo)
        
        book_list = []
        # returning a book
        if cardNo != None:
            i = 0
            for b in book_dictionary:
                if (get_num_copies(self.cursor, branch, book_dictionary[b][0])) > 0:
                    book_list.append(book_dictionary[b][1])

                    author_dict = get_authors_by_book(self.cursor, b)
                    j = 0
                    for a in author_dict:
                        if j == 0:
                            book_list[i] += ' by '
                        elif j < len(author_dict):
                            book_list[i] += ' and '
                        book_list[i] += author_dict[a][1]
                        j += 1
                    i += 1
        # checking out a book
        else:
            if fromUpdateBook:
                i = 0
                for b in book_dictionary:
                    book_list.append(book_dictionary[b][1])

                    author_dict = get_authors_by_book(self.cursor, b)
                    j = 0
                    for a in author_dict:
                        if j == 0:
                            book_list[i] += ' by '
                        elif j < len(author_dict):
                            book_list[i] += ' and '
                        book_list[i] += author_dict[a][1]
                        j += 1
                    i += 1
            else:
                i = 0
                for b in book_dictionary:
                    # check books available and not all on loan
                    if (get_num_copies(self.cursor, branch, book_dictionary[b][0]) - get_num_books_on_loan(self.cursor, branch, book_dictionary[b][0])) > 0:
                        book_list.append(book_dictionary[b][1])

                        author_dict = get_authors_by_book(self.cursor, b)

                        j = 0
                        for a in author_dict:
                            if j == 0:
                                book_list[i] += ' by '
                            elif j < len(author_dict):
                                book_list[i] += ' and '
                            book_list[i] += author_dict[a][1]
                            j += 1
                        i += 1
                            

        book_selection = self.prompt_options(book_list)

        if isinstance(book_selection, bool):
            if book_selection == True:
                return True
            else:
                print('returning false from user book selection')
                return False

        return book_dictionary[book_selection]

    def get_branch_selection(self):
        while True:
            branch_dictionary = get_branches(self.cursor)
            
            branch_list = []
            i = 0
            for b in branch_dictionary:
                branch_list.append(branch_dictionary[b][1])
                branch_list[i] = branch_list[i] + ', ' + branch_dictionary[b][2]
                i += 1

            branch_selection = self.prompt_options(branch_list)
        
            if isinstance(branch_selection, bool):
                if branch_selection == True:
                    return True
                else:
                    return False


            return branch_dictionary[branch_selection]

    def get_branches(self):
        branch_dictionary = get_branches(self.cursor)            
        branch_list = []
        for b in branch_dictionary:
            branch_list.append(Branch(branch_dictionary[b][0], branch_dictionary[b][1], branch_dictionary[b][2]))
        return branch_list

    def print_menu(self, menu):
        print('\n')
        print(constants.MENU_LINE_BREAK)
        print(menu, constants.bcolor.get_color('header', 'Menu'))
        print(constants.LINE_BREAK)

    def print_submenu(self, submenu):
        print('\n')
        print(submenu)
        print(constants.LINE_BREAK)

    def prompt_options(self, options, option_functions=None):
        while True:
            i = 1
            for opt in options:
                print(i, ') ', opt)
                i += 1

            if i == 1:
                print(constants.bcolor.get_color('red', 'No data available.'))

            # Get quit to previous menu opt
            prev_menu_opt = i
            print(prev_menu_opt, ') ', constants.PREVIOUS_MENU)

            # grab selection
            selection = self.get_selection()

            # ensure selection is an int
            if selection.isdigit():
                selection = int(selection)

            # quit program
            if selection == 'quit':
                return False
            # go to previous menu
            elif selection == prev_menu_opt:
                print(constants.bcolor.get_color('green', 'Returning to prev menu'))
                return True
            # proceed with a function
            elif selection in range(1, len(options)+2):
                if not option_functions:
                    return selection
                else:
                    func = option_functions.get(selection)
                    continue_prompt = func()
                    if not continue_prompt:
                        return False
            else:
                print(constants.INCORRECT_INPUT)

        
