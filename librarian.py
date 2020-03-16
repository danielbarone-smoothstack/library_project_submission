import constants
from user import User 
from library_objects import Branch, Book

class Librarian(User):

    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.user_type = constants.bcolor.get_color('header', 'Librarian')

    def __str__(self):
        return self.user_type

    def update_lib_details(self, branch_selection):
        branch_id = branch_selection.branchId
        branch_name = branch_selection.branchName
        branch_address = branch_selection.branchAddress

        submenu = 'You have chosen to update the branch with\nBranch ID: ' + \
            str(branch_id) + ' and Branch Name: ' + branch_name + \
                '.\nEnter \'quit\' at any prompt to cancel operation.'
        self.print_submenu(submenu)

        name_input = ''
        while True:
            name_input = input('Please enter new branch name or enter N/A for no change: ')
            if name_input == 'quit':
                return True
            elif len(name_input) == 0 or name_input == 'N/A':
                name_input = branch_name
                break
            else:
                break
        address_input = ''
        while True:
            address_input = input('Please enter new branch address or enter N/A for no change: ')
            if name_input == 'quit':
                return True
            elif len(address_input) == 0 or name_input == 'N/A':
                address_input = branch_address
                break
            else:
                break
        

        updated_branch = Branch(branch_id, name_input, address_input)

        updated_branch.update_branch(self.cursor, self.connection)

        return True
            
    def add_copies(self, branch_selection):
        self.print_submenu('\nPick the Book you want to add copies of')

        book_list = branch_selection.get_books_by_branch_id(self.cursor)

        book_selection = self.prompt_options(book_list)

        if isinstance(book_selection, bool):
            if book_selection == True:
                return True
            else: 
                return False

        if book_list[book_selection-1]:
            num_copies = book_list[book_selection-1].get_num_copies(branch_selection.branchId)

            cur_num_copies = ('\nExisting number of copies: ' + str(num_copies))
            self.print_submenu(cur_num_copies)
            new_num_copies = input('Enter new number of copies: ')

            if new_num_copies.isdigit():
                new_num_copies = int(new_num_copies)

                # UPDATE NUM COPIES
                book_list[book_selection-1].update_num_of_copies(
                    self.connection, 
                    branch_selection.branchId, 
                    new_num_copies
                )
                return True
            elif new_num_copies == 'quit':
                return False
            else:
                print(constants.INCORRECT_INPUT)
                return True
    # Update copies or library deets
    def LIB3(self, branch_selection):

        while True:
            # Get user selection
            LIB3_selection = self.prompt_options(constants.LIB3_OPTIONS)

            if isinstance(LIB3_selection, bool):
                if LIB3_selection == True:
                    return True
                else:
                    return False

            # update details of library
            if LIB3_selection == 1:
                return self.update_lib_details(branch_selection)

            # Add copies
            elif LIB3_selection == 2:
                return self.add_copies(branch_selection)

    # User selects branch
    def LIB2(self):
        while True:
            self.print_submenu('Select a Branch')
            branch_list = self.get_branches()
            LIB2_selection = self.prompt_options(branch_list)
            if isinstance(LIB2_selection, bool):
                if LIB2_selection == True:
                    return True
                else:
                    return False
            continue_LIB2 = self.LIB3(branch_list[LIB2_selection-1]) 
            if not continue_LIB2:
                return False

    # Main Librarian Driver
    def driver(self):
        LIBRARIAN_OPTIONS = {
            1: self.LIB2,
        }
        self.print_menu(self.user_type)
        return self.prompt_options(constants.LIB1_OPTIONS, LIBRARIAN_OPTIONS)
