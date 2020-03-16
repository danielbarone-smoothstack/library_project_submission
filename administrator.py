from procedures import (
    get_branches,
    admin_add_book_and_author,
    admin_update_book_and_author,
    admin_delete_book_and_author,
    get_authors_by_book,
    get_all_books,
    add_branch,
    # update_branch,
    delete_branch,
    modify_publisher,
    get_all_publishers,
    # change_DueDate,
    modify_borrower,
    get_borrower,
    check_existing_loans,
    remove_single_book_author_link,
    add_to_tbl_copies,
    get_book_from_author_title
)
import constants
from user import User
from library_objects import Publisher, BookLoan, Branch

class Administrator(User):

    def __init__(self, cursor, connection):
        super().__init__(cursor, connection)
        self.user_type = constants.bcolor.get_color('header', 'Administrator')

    def __str__(self):
        return self.user_type

    def override_duedate(self):
        bookId = ''
        while True:
            bookId = input('Enter Book ID: ')
            if len(bookId) == 0:
                print('ERROR: You must enter a value. Type \'quit\' to quit program.')
            elif bookId == 'quit':
                return False
            elif len(bookId) > 0:
                break
        
        branchId = ''
        while True:
            branchId = input('Enter Branch ID: ')
            if len(branchId) == 0:
                print('ERROR: You must enter a value. Type \'quit\' to quit program.')
            elif branchId == 'quit':
                return False
            elif len(branchId) > 0:
                break
        
        cardNo = ''
        while True:
            cardNo = input('Enter Card Number: ')
            if len(cardNo) == 0:
                print('ERROR: You must enter a value. Type \'quit\' to quit program.')
            elif cardNo == 'quit':
                return False
            elif len(cardNo) > 0:
                break
        
        newDate = ''
        while True:
            newDate = input('Enter New Due Date: ')
            if len(newDate) == 0:
                print('ERROR: You must enter a value. Type \'quit\' to quit program.')
            elif newDate == 'quit':
                return False
            elif len(newDate) > 0:
                break

        # NOTE TO RORY: handle the int type conversions below in your update plz
        book_loan = BookLoan(int(bookId), int(branchId), int(cardNo))
        book_loan.change_DueDate(self.cursor, self.connection, newDate)
        return True


    def aud_borrowers(self):
        self.print_submenu('A/U/D Borrower Menu')

        AUD_OPTIONS = {
            1: self.a__borrower,
            2: self.u__borrower,
            3: self.d__borrower
        }
        return self.prompt_options(constants.AUD_BORROWER_OPTIONS, AUD_OPTIONS)

    def a__borrower(self):
        self.print_submenu('Add a Borrower')

        name = ''
        address = ''
        phone = ''
        while True:
            name = input('Enter Borrower Name: ')
            if len(name) == 0:
                print('ERROR: You must enter a name. Type \'quit\' to quit program.')
            elif name == 'quit':
                return False
            elif len(name) > 0:
                break
        while True:
            address = input('Enter Borrower Address: ')
            if len(address) == 0:
                print('ERROR: You must enter an address. Type \'quit\' to quit program.')
            elif address == 'quit':
                return False
            elif len(address) > 0:
                break

        while True:
            phone = input('Enter Borrower Phone Number: ')
            if len(phone) == 0:
                print('ERROR: You must enter an phone number. Type \'quit\' to quit program.')
            elif phone == 'quit':
                return False
            elif len(phone) > 0:
                break

        modify_borrower(self.cursor, self.connection, 'A', 0, name, address, phone)

        return True
    def u__borrower(self):
        self.print_submenu('Update a Borrower')

        cardNo = None
        while True:
            cardNo = input('Enter the card number for the\nborrower you want to update: ')

            if len(cardNo) > 0 and cardNo.isdigit():
                cardNo = int(cardNo)
                break
            else:
                print(constants.INCORRECT_INPUT)

        borrower_info = get_borrower(self.cursor, cardNo) # {id: [name, address, phone]}

        old_id = None
        old_name = None
        old_address = None
        old_phone = None
        if borrower_info:
             for b in borrower_info:
                 old_id = b
                 old_name = borrower_info[b][0]
                 old_address = borrower_info[b][1]
                 old_phone = borrower_info[b][2]
        else:
            print('No such user with that card number exists.\nReturning to previous menu.')
            return True

        borrower_string = 'Editing borrower ' + old_name + '\n' + old_address + '\n' + old_phone
        self.print_submenu(borrower_string)

        new_name = input('Enter a new name or leave blank to continue: ')
        new_address = input('Enter new address or leave blank to continue: ')
        new_phone = input('Enter a new phone number or leave blank to continue: ')

        if len(new_name) > 0:
            old_name = new_name
        if len(new_address) > 0:
            old_address = new_address
        if len(new_phone) > 0:
            old_phone = new_phone

        modify_borrower(self.cursor, self.connection, 'U', old_id, old_name, old_address, old_phone)

        return True

    def d__borrower(self):
        self.print_submenu('Delete a borrower')

        cardNo = None
        while True:
            cardNo = input('Enter the card number for the\nborrower you want to delete: ')

            if len(cardNo) > 0 and cardNo.isdigit():
                cardNo = int(cardNo)
                break
            else:
                print(constants.INCORRECT_INPUT)

        borrower_info = get_borrower(self.cursor, cardNo) # {id: [name, address, phone]}

        old_id = None
        old_name = None
        old_address = None
        old_phone = None
        if borrower_info:
             for b in borrower_info:
                 old_id = b
                 old_name = borrower_info[b][0]
                 old_address = borrower_info[b][1]
                 old_phone = borrower_info[b][2]
        else:
            print('No such user with that card number exists.\nReturning to previous menu.')
            return True

        borrower_string = 'Deleting borrower ' + old_name + '\n' + old_address + '\n' + old_phone
        self.print_submenu(borrower_string)

        print('Are you sure you wish to delete this borrower?')
        delete_options = ['Yes', 'No']

        delete_selection = self.prompt_options(delete_options)

        if isinstance(delete_selection, bool):
            if delete_selection == True:
                return True
            elif delete_selection == False:
                return False

        if int(delete_selection) == 1:
            print('Deleting borrower', old_name)

            existing_loans = check_existing_loans(self.cursor, old_id)
            if existing_loans:
                print('Failed to delete borrower with existing book loans.\n')
            else:
                modify_borrower(self.cursor, self.connection, 'D', old_id, old_name, old_address, old_phone)
        else:
            print('Not deleting borrower.')

        return True


    def aud_publishers(self):
        PUBLISHER_AUD_FUNCTIONS = {
            1: self.a__publisher,
            2: self.u__publisher,
            3: self.d__publisher
        }
        return self.prompt_options(constants.PUBLISHER_OPTIONS, PUBLISHER_AUD_FUNCTIONS)
    def a__publisher(self):

        new_publisher_name = ''
        while True:
            new_publisher_name = input('Enter Publisher Name: ')
            if len(new_publisher_name) == 0:
                print('ERROR: You must enter a name')
            elif new_publisher_name == 'quit':
                return False
            else:
                break

        new_publisher_address = ''
        while True:
            new_publisher_address = input('Enter Publisher Address: ')
            if len(new_publisher_address) == 0:
                print('ERROR: You must enter an address')
            elif new_publisher_address == 'quit':
                return False
            else:
                break

        new_publisher_phone = ''
        while True:
            new_publisher_phone = input('Enter Publisher Phone: ')
            if len(new_publisher_address) == 0:
                print('ERROR: You must enter a phone number')
            elif new_publisher_address == 'quit':
                return False
            else:
                break
        
        new_publisher = Publisher(0, new_publisher_name, new_publisher_address, new_publisher_phone)
        new_publisher.modify_publisher(self.cursor, self.connection, 'A')

        return True
    def u__publisher(self):
        publisher_dictionary = get_all_publishers(self.cursor)
        publisher_list = []

        for pub in publisher_dictionary:
            publisher_list.append(Publisher(
                publisher_dictionary[pub][0], 
                publisher_dictionary[pub][1],
                publisher_dictionary[pub][2],
                publisher_dictionary[pub][3],
            ))

        pub_selection = self.prompt_options(publisher_list)

        if isinstance(pub_selection, bool):
            if pub_selection == True:
                return True
            else:
                return False

        old_name = publisher_list[pub_selection-1].publisherName

        new_name = input('Edit publisher name or press enter to contine: ')
        if len(new_name) == 0:
            new_name = old_name
        if new_name == 'quit':
            return False

        new_address = input('Edit address or press enter to continue: ')
        if len(new_address) == 0:
            new_address = publisher_list[pub_selection-1].publisherAddress
        if new_address == 'quit':
            return False

        new_phone = input('Edit phone or press enter to continue: ')
        if len(new_phone) == 0:
            new_phone = publisher_list[pub_selection-1].publisherPhone
        if new_address == 'quit':
            return False

        new_publisher = Publisher(
            publisher_list[pub_selection-1].publisherId, 
            new_name,
            new_address,
            new_phone
        )

        new_publisher.modify_publisher(self.cursor, self.connection, 'U')

        print('Updated Publisher Information.')

        return True
    def d__publisher(self):
        publisher_dictionary = get_all_publishers(self.cursor)
        publisher_list = []

        for pub in publisher_dictionary:
            publisher_list.append(Publisher(
                publisher_dictionary[pub][0], 
                publisher_dictionary[pub][1],
                publisher_dictionary[pub][2],
                publisher_dictionary[pub][3],
            ))

        pub_selection = self.prompt_options(publisher_list)

        if isinstance(pub_selection, bool):
            if pub_selection == True:
                return True
            else:
                return False

        old_name = publisher_list[pub_selection-1].publisherName

        publisher_list[pub_selection-1].modify_publisher(
            self.cursor, 
            self.connection, 
            'D', 
        )

        print('Deleted Publisher Information')

        return True



    def aud_library_branches(self):
        BRANCH_AUD_OPTIONS = {
            1: self.a_branch,
            2: self.u_branch,
            3: self.d_branch
        }
        return self.prompt_options(constants.ADMIN_BRANCH_OPTIONS, BRANCH_AUD_OPTIONS)
    # Helpers aud_library_branches
    def a_branch(self):
        branchNameIsValid = False
        branchAddressIsValid = False
        while branchNameIsValid == False :
            branchName = input('New branch name: ')
            if branchName == 'quit' :
                return False
            elif len(branchName) > 0 and len(branchName) <= 45:
                branchNameIsValid = True
        while branchAddressIsValid == False :
            branchAddress = input('New branch address: ')
            if branchAddress == 'quit' :
                return False
            elif len(branchAddress) > 0 and len(branchName) <= 45:
                branchAddressIsValid = True

        new_branch = Branch(None, branchName, branchAddress)
        new_branch.add_branch(self.cursor, self.connection)
        print('\nNew library branch successfully added.\n')
        return True

    def u_branch(self):
        self.print_submenu('Update Library Branches')

        branch_list = self.get_branches()
        branch_selection = self.prompt_options(branch_list)
        
        if isinstance(branch_selection, bool):
            if branch_selection == True:
                return True
            elif branch_selection == False:
                return False
                
        branchName = input('Branch name (or N/A to leave as-is):\n')
        if branchName == 'quit':
            return True
        branchAddress = input('Branch address (or N/A to leave as-is):\n')
        if branchAddress == 'quit' :
            return True
        
        updated_branch = Branch(branch_list[branch_selection-1].branchId, branchName, branchAddress)
        updated_branch.update_branch(self.cursor, self.connection)

        return True

    def d_branch(self):
        bs = self.get_branch_selection()
        if isinstance(bs, bool):
            if bs == True:
                return True
            else:
                return False
        branchId = bs[0]
        branch_to_delete = Branch(branchId, '', '')
        if branch_to_delete.delete_branch(self.cursor, self.connection):
            print('Successfully deleted: ', bs[1])
        return True

    '''
    Method: aud_book_and_author
    Desc:   Add/Update/Delete Book and Author
    '''
    def aud_book_and_author(self):

        self.print_submenu('Book and Author Menu')

        AUD_OPTIONS = {
            1: self.a__book_and_author,
            2: self.u__book_and_author,
            3: self.d__book_and_author
        }
        return self.prompt_options(constants.ADMIN_BOOK_AND_AUTHOR_OPTIONS, AUD_OPTIONS)

    ''' Helper method: Add book and author '''
    def a__book_and_author(self):

        self.print_submenu('Add a Book and Author')

        # Add by branch || Add generally 
        ADD_OPTIONS = [constants.bcolor.get_color('blue', 'Add by branch'), constants.bcolor.get_color('blue', 'Add without specifying a branch')]

        add_method = self.prompt_options(ADD_OPTIONS)

        if isinstance(add_method, bool):
            if add_method == False:
                return False
            elif add_method == True:
                return True

        branch_selection = None
        # Add by branch selected
        if add_method == 1:
            # Get branch selection 
            branch_selection = self.get_branch_selection() # [1, 'New Sharpstown', 'New Sharpstown Address']

            if isinstance(branch_selection, bool):
                if branch_selection == True:
                    return True
                else:
                    return False
        # Get new book title
        new_book_title = ''
        while True:
            new_book_title = input('Input new book title: ')
            if len(new_book_title) == 0:
                print(constants.INCORRECT_INPUT)
                print('Name cannot be blank')
            elif new_book_title == 'quit':
                return False
            else:
                break
        # Get new book's authors
        authors = []
        while True:
            new_book_author = ''
            while True:
                new_book_author = input('Input book author: ')
                if len(new_book_author) == 0:
                    print(constants.INCORRECT_INPUT)
                    print('Author cannot be blank')
                elif new_book_author == 'quit':
                    return False
                else:
                    break

            authors.append(new_book_author)

            print(constants.ADD_MORE_AUTHORS)
            cont_add_authors = input(constants.MAKE_SELECTION)

            if cont_add_authors.isdigit():
                if int(cont_add_authors) == 2:
                    break
            elif cont_add_authors == 'quit':
                return False
            else:
                print(constants.INCORRECT_INPUT)

        if len(authors) > 1:
            print('Adding', len(authors), 'authors to', new_book_title)

        # Invoke sql procedure
        for author in authors:
            print('Adding', author, 'to', new_book_title)
            admin_add_book_and_author(self.cursor, self.connection, new_book_title, author)

        # if add to library branch, 
        if add_method == 1:
            num_copies = input('How many copies do you want to add to this library branch: ')

            if num_copies.isdigit():
                bookId = get_book_from_author_title(self.cursor, authors[0], new_book_title)
                add_to_tbl_copies(self.cursor, self.connection, bookId, branch_selection[0], num_copies)
            else:
                print(constants.INCORRECT_INPUT)
                print('Adding 0 for number of copies for this book.')
                bookId = get_book_from_author_title(self.cursor, authors[0], new_book_title)
                add_to_tbl_copies(self.cursor, self.connection, bookId, branch_selection[0], 0)

        return True

    ''' Helper method: Update book and author '''
    '''
    first- book ID to be used as a look-up reference
    second- Author ID for same
    third- String containing the new title(limited to 45 chars)
    fourth- int specifying the new foreign key linking the publisher table
    fifth- String containing new author name(same 45 char limit)
    '''
    def u__selected_book(self, selection, book_dictionary):

        pubID = book_dictionary[selection][1]

        update_book_title = input('\nEnter new book title or click enter to leave unchanged: ')

        new_title = book_dictionary[selection][0]
        # if title altered, update title
        if len(update_book_title) > 0:
            new_title = update_book_title

        loop_count = 0
        while True:
            author_dictionary = get_authors_by_book(self.cursor, selection)
            author_list = []
            author_id_list = []
            for author in author_dictionary:
                author_list.append(author_dictionary[author][1])
                author_id_list.append(author_dictionary[author][0])

            if loop_count == 0:
                print('\nWould you like to update an author for this book?')
                loop_count += 1
            else:
                print('\nWould you like to continue updating authors for this book?')

            UPD_AUTH_OPT = ['Yes', 'No']
            upd_auth_selection = self.prompt_options(UPD_AUTH_OPT)

            if isinstance(upd_auth_selection, bool):
                if upd_auth_selection == True:
                    return True
                else:
                    return False

            if upd_auth_selection == 2:
                print(constants.LINE_BREAK)
                print('Only updating title...')
                print(constants.LINE_BREAK)
                admin_update_book_and_author(
                    self.cursor,
                    self.connection,
                    selection,
                    author_id_list[0],
                    new_title,
                    pubID,
                    author_list[0]
                )
                break

            print('\nWhich author would you like to update?')
            author_selection = self.prompt_options(author_list)

            if isinstance(author_selection, bool):
                if author_selection == True:
                    return True
                else:
                    return False

            if isinstance(author_selection, int):
                print(constants.LINE_BREAK)
                print('You are updating author', author_list[author_selection-1])
                update_author_name = input('Enter new author name or type \'delete\' to remove author, or click enter to proceed: ')

                new_author = author_dictionary[author_selection][1]
                if len(update_author_name) > 0:
                    if update_author_name == 'delete':
                        remove_single_book_author_link(
                            self.cursor,
                            self.connection,
                            selection,
                            author_dictionary[author_selection][0]
                        )
                        print('Saving changes...')
                    else:
                        new_author = update_author_name

                # sql update
                admin_update_book_and_author(
                    self.cursor,
                    self.connection,
                    selection,
                    author_dictionary[author_selection][0],
                    new_title,
                    pubID,
                    new_author
                )
            elif author_selection == True:
                return True
            else:
                return False

        return True

    def u__book_and_author(self):
        self.print_submenu('Update Book and Author')

        update_options = ['Update by Branch', 'Update without specifying a Branch']
        
        update_method = self.prompt_options(update_options)

        if isinstance(update_method, bool):
            if update_method == False:
                return False
            elif update_method == True:
                return True

        branch_selection = None
        book_selection = None
        # Add by branch selected
        if update_method == 1:
            # Get branch selection 
            print(constants.LINE_BREAK)
            print('Which branch do you want to select a book from?')
            branch_selection = self.get_branch_selection() # [1, 'New Sharpstown', 'New Sharpstown Address']

            if isinstance(branch_selection, bool):
                if branch_selection == False:
                    return False
                elif branch_selection == True:
                    return True

            print('Which book do you want to update?')
            book_selection = self.get_book_selection(branch_selection[0], None, True) # [id, title]

            if isinstance(branch_selection, bool):
                if branch_selection == True:
                    return True
                else:
                    return False    

            if isinstance(book_selection, bool):
                if book_selection == True:
                    return True
                else:
                    return False

            book_dictionary = get_all_books(self.cursor)
            pubID = book_dictionary[book_selection[0]][1]

            old_title = book_selection[1]
            new_title_prompt = 'Enter new title for ' + old_title + ': '
            new_title = input(new_title_prompt)

            if len(new_title) == 0:
                new_title = old_title

            loop_count = 0
            while True:
                author_dictionary = get_authors_by_book(self.cursor, book_selection[0])
                author_list = []
                author_id_list = []
                for author in author_dictionary:
                    author_list.append(author_dictionary[author][1])
                    author_id_list.append(author_dictionary[author][0])

                if loop_count == 0:
                    print('\nWould you like to update an author for this book?')
                    loop_count += 1
                else:
                    print('\nWould you like to continue updating authors for this book?')

                UPD_AUTH_OPT = ['Yes', 'No']
                upd_auth_selection = self.prompt_options(UPD_AUTH_OPT)

                if isinstance(upd_auth_selection, bool):
                    if upd_auth_selection == True:
                        return True
                    else:
                        return False

                if upd_auth_selection == 2:
                    print(constants.LINE_BREAK)
                    print('Only updating title...')
                    print(constants.LINE_BREAK)
                    admin_update_book_and_author(
                        self.cursor,
                        self.connection,
                        book_selection[0],
                        author_id_list[0],
                        new_title,
                        pubID,
                        author_list[0]
                    )
                    return True

                print('\nWhich author would you like to update?')
                author_selection = self.prompt_options(author_list)

                if isinstance(author_selection, bool):
                    if author_selection == True:
                        return True
                    else:
                        return False

                if isinstance(author_selection, int):
                    print(constants.LINE_BREAK)
                    print('You are updating author', author_list[author_selection-1])
                    update_author_name = input('Enter new author name or type \'delete\' to remove author, or click enter to proceed: ')

                    new_author = author_dictionary[author_selection][1]
                    if len(update_author_name) > 0:
                        if update_author_name == 'delete':
                            remove_single_book_author_link(
                                self.cursor,
                                self.connection,
                                book_selection[0],
                                author_dictionary[author_selection][0]
                            )
                            print('Saving changes...')
                        else:
                            new_author = update_author_name

                    # sql update
                    admin_update_book_and_author(
                        self.cursor,
                        self.connection,
                        book_selection[0],
                        author_dictionary[author_selection][0],
                        new_title,
                        pubID,
                        new_author
                    )
                elif author_selection == True:
                    return True
                else:
                    return False

            return True

        else:
            book_dictionary = get_all_books(self.cursor)

            print(constants.LINE_BREAK)
            print('Which book do you want to update?')

            book_selections = []
            for book in book_dictionary:
                book_selections.append(book_dictionary[book][0])

            selection = self.prompt_options(book_selections)

            if isinstance(selection, bool):
                if selection == True:
                    return True
                else:
                    return False

            if isinstance(selection, int):
                return self.u__selected_book(selection, book_dictionary)
            else:
                return False


    ''' Helper method: Delete book and author '''
    def d__book_and_author(self):
        delete_options = ['Delete by Branch', 'Delete without specifying a Branch']
        
        delete_method = self.prompt_options(delete_options)

        if isinstance(delete_method, bool):
            if delete_method == False:
                return False
            elif delete_method == True:
                return True

        branch_selection = None
        book_selection = None
        # Add by branch selected
        if delete_method == 1:
            # Get branch selection 
            print(constants.LINE_BREAK)
            print('Which branch do you want to delete a book from?')
            branch_selection = self.get_branch_selection() # [1, 'New Sharpstown', 'New Sharpstown Address']

            if isinstance(branch_selection, bool):
                if branch_selection == True:
                    return True
                else:
                    return False  
            
            print('Which book do you want to delete?')
            book_selection = self.get_book_selection(branch_selection[0], None, True) # [id, title]

            if isinstance(book_selection, bool):
                if book_selection == True:
                    return True
                else:
                    return False

            admin_delete_book_and_author(self.cursor, self.connection, book_selection[0])
            return True
        else:

            book_dictionary = get_all_books(self.cursor)
            book_corrected_dictionary = {}

            i = 1
            for b in book_dictionary:
                book_corrected_dictionary[i] = [b, book_dictionary[b][0], book_dictionary[b][1]]
                i += 1
            
            self.print_submenu('Which book do you want to delete?')

            book_selections = []
            for book in book_dictionary:
                book_selections.append(book_dictionary[book][0])

            selection = self.prompt_options(book_selections)

            if isinstance(selection, bool):
                if selection == True:
                    return True
                elif selection == False:
                    return False

            if isinstance(selection, int):
                admin_delete_book_and_author(self.cursor, self.connection, book_corrected_dictionary[selection][0])
                return True
            else:
                return False

    '''
    Method: driver
    Desc:   Main entry point to administrator
            functionality.
    '''
    def driver(self):

        ADMIN_OPTIONS = {
            1: self.aud_book_and_author,
            2: self.aud_publishers,
            3: self.aud_library_branches,
            4: self.aud_borrowers,
            5: self.override_duedate
        }

        self.print_menu(self.user_type)

        return self.prompt_options(constants.MAIN_ADMIN_OPTIONS, ADMIN_OPTIONS)

