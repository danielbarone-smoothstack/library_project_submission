import mysql.connector
from mysql.connector import errorcode
import getpass
import constants

# import credentials

def sql_connect():

    print('\nEnter database credentials')

    username=input('Username: ')
    password=getpass.getpass(prompt='Password: ')

    try:
        cnx = mysql.connector.connect(user=username, password=password,
                                host='127.0.0.1',
                                database='library')
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
            return False
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
            return False
        else:
            print(err)
            return False
    else:
        cur = cnx.cursor()
        return [cnx, cur]

def sql_close(cnx, cursor):
    cursor.close()
    cnx.close()

def checkout_book(cursor, connection, bookId, branchId, cardNo):
    args = (bookId, branchId, cardNo)
    cursor.callproc('checkout_book', args)
    connection.commit()

def get_branches(cursor):
    cursor.callproc('getBranches', args=())

    branch_dictionary = {}

    for result in cursor.stored_results():

        branches = result.fetchall()

        i = 1
        for branch in branches:
            branch_dictionary[i] = [branch[1], branch[0], branch[2]]
            i+=1

    return branch_dictionary

def get_all_books(cursor):
    cursor.callproc('getAllBooks', args=())

    # bookId: [title, pubId]
    book_dictionary = {}

    for result in cursor.stored_results():
        books = result.fetchall()
        for book in books:
            book_dictionary[book[0]] = [book[1], book[2]]

    return book_dictionary

def get_books_by_branch_id(cursor, branchId):

    args = (branchId,)

    cursor.callproc('get_books_by_branch_id', args)

    book_dictionary = {}

    for result in cursor.stored_results():

        books = result.fetchall()

        i = 1
        for book in books:
            book_dictionary[i] = [book[0], book[1]]
            i+=1

    return book_dictionary

def get_num_copies(cursor, branchId, bookId):

    args = (branchId,bookId,)

    cursor.callproc('get_num_copies', args)

    number_of_copies = 0

    for result in cursor.stored_results():

        num_copies = result.fetchall()

        for num in num_copies:
            number_of_copies = num[0]


    return number_of_copies

def get_num_copies_remaining(cursor, branchId, bookId):
    args = (branchId,bookId,)

    cursor.callproc('get_num_copies_remaining', args)

    number_of_copies = 0

    for result in cursor.stored_results():

        num_copies = result.fetchall()

        for num in num_copies:
            number_of_copies = num[0]


    return number_of_copies

def get_num_books_on_loan(cursor, branchId, bookId):
    args = (branchId, bookId, )
    cursor.callproc('get_num_books_on_loan', args)

    num_books_on_loan = 0

    for result in cursor.stored_results():

        num_loans = result.fetchall()

        for num in num_loans:
            num_books_on_loan = num[0]

    return num_books_on_loan

def update_num_of_copies(cursor, connection, bookId, branchId, newNumOfCopies):

    args = (bookId, branchId, newNumOfCopies,)

    cursor.callproc('updateNoOfCopies', args)

    connection.commit()

def add_to_tbl_copies(cursor, connection, bookId, branchId, newNumOfCopies):

    args = (bookId, branchId, newNumOfCopies,)

    cursor.callproc('add_to_tbl_copies', args)

    connection.commit()

def get_book_from_author_title(cursor, author_name, book_title):

    args = (author_name, book_title,)

    cursor.callproc('get_book_from_author_title', args)

    bookId = None 

    for result in cursor.stored_results():

        num_books = result.fetchall()

        for book in num_books:
            bookId = book[0]
            print(book)
    
    return bookId

def modify_publisher(cursor, connection, param_operation, pubId, new_name, new_address, new_phone):
    cursor.execute('select Admin_Modify_Publisher(%s, %s, %s, %s, %s)', (param_operation, pubId, new_name, new_address, new_phone))

    rows = cursor.fetchall()
    results = len(rows)
    ret = ''
    if results > 0:
        row = rows[0]
        ret = row[0]

    connection.commit()
    return ret

def get_all_publishers(cursor):

    cursor.callproc('get_all_publishers', args=())

    publisher_dictionary = {}

    i = 1
    for result in cursor.stored_results():
        publishers = result.fetchall()
        for publisher in publishers:
            publisher_dictionary[i] = [publisher[0], publisher[1], publisher[2], publisher[3]]
            i += 1
    return publisher_dictionary

def get_authors_by_book(cursor, bookId):

    args = (bookId,)

    cursor.callproc('get_authors_from_book', args)

    authors_dictionary = {}

    i = 1
    for result in cursor.stored_results():
        authors = result.fetchall()
        for author in authors:
            authors_dictionary[i] = [author[0], author[1]]
            i += 1

    return authors_dictionary

def admin_add_book_and_author(cursor, connection, new_book_name, new_author_name):

    args = (new_book_name, new_author_name,)

    cursor.callproc('admin_add_book_and_author', args)

    connection.commit()

def admin_update_book_and_author(cursor, connection, bookID, authorID, newTitle, newPublisherID, newAuthorName):

    args = (bookID, authorID, newTitle, newPublisherID, newAuthorName,)

    cursor.callproc('admin_update_book_and_author', args)

    connection.commit()

def admin_delete_book_and_author(cursor, connection, bookID):

    args = (bookID,)

    cursor.callproc('admin_delete_book_and_author', args)

    connection.commit()

# param checking helper
def is_valid_int(p):
    if p > 2147483647 or p < 1:
        return False
    else:
        return True

def is_valid_varchar_45(p):
    if len(p) > 45:
        return False
    else:
        return True

def card_number_exists(cursor, cn):
    # if not is_valid_int(cn):
    #     return ''
    args = (cn,)
    cursor.callproc('card_number_exists', args)

    card_exists = False

    card_number = []
    for result in cursor.stored_results():
        cardRows = result.fetchall()

        for cardRow in cardRows:
            card_number.append(cardRow[0])

    if len(card_number) == 1 and card_number[0] == cn:
        card_exists = True

    return card_exists


def get_books_due(cursor, cardNo):
    # if not is_valid_int(cardNo):
    #     return ''
    args = (cardNo,)
    cursor.callproc('get_books_due', args)
    books = {}
    for result in cursor.stored_results():
        i = 1
        for row in result.fetchall():
            books[i] = [row[0],row[1]]
    return books


def borrower_return_book(cursor, connection, bookId, branchId, cardNo):
    cursor.execute('select Borrower_Return_Book_test_proc(%s, %s, %s)', (bookId, branchId, cardNo))
    rows = cursor.fetchall()
    results = len(rows)
    ret = ''
    if results > 0:
        row = rows[0]
        ret = row[0]
    print(ret)
    connection.commit()
    return True

def add_branch(cursor, connection, branchName, branchAddress):
    action = 'A'
    branchId = 0 # updated in MySQL stored procedure.
    args = (action, branchId, branchName, branchAddress,)
    cursor.callproc('admin_branches', args)
    connection.commit()

def update_branch(cursor, connection, branchId, branchName, branchAddress):
    action = 'U'
    args = (action, branchId, branchName, branchAddress,)
    cursor.callproc('admin_branches', args)
    connection.commit()

def delete_branch(cursor, connection, branchId):
    action = 'D'
    args = (action, branchId, '', '',)
    cursor.callproc('admin_branches', args)
    connection.commit()
    return True

def change_DueDate(cursor, connection, bookId, branchId, cardNo, newDate):
    if not is_valid_int(bookId):
        return ''
    if not is_valid_int(branchId):
        return ''
    if not is_valid_int(cardNo):
        return ''
    cursor.execute('select Admin_Override_Due_Date(%s, %s, %s, %s)', (bookId, branchId, cardNo, newDate))
    rows = cursor.fetchall()
    results = len(rows)
    ret = ''
    if results > 0:
        row = rows[0]
        ret = row[0]

    connection.commit()
    return ret


# AUD Borrower
def modify_borrower(cursor, connection, operation, cardNo, name, address, phone):
    args = (operation, cardNo, name, address, phone, '',)

    cursor.callproc('Modify_Borrower', args)

    connection.commit()

def get_borrower(cursor, cardNo):

    args = (cardNo, )

    cursor.callproc('get_borrower', args)

    borrower_dictionary = {}

    for result in cursor.stored_results():

        borrower = result.fetchall()
        for b in borrower:
            borrower_dictionary[b[0]] = [b[1], b[2], b[3]]

    return borrower_dictionary

def check_existing_loans(cursor, cardNo):
    args = (cardNo,)

    cursor.callproc('check_existing_loans', args)

    book_loans = {}


    for result in cursor.stored_results():

        loans = result.fetchall()

        i = 1
        for l in loans:
            book_loans[i] = [l[0], l[1], l[2], l[3], l[4]]
            i += 1

    if len(book_loans) > 0:
        return True
    else:
        return False

def duplicate_loan_check(cursor, connection, bookId, branchId, cardNo):
    cursor.execute('select duplicate_loan_check(%s, %s, %s)', (bookId, branchId, cardNo))
    rows = cursor.fetchall()
    results = len(rows)
    ret = ''
    if results > 0:
        row = rows[0]
        ret = row[0]

    connection.commit()
    return ret

def remove_single_book_author_link(cursor, connection, bookId, authorId):
    args = (bookId, authorId)
    cursor.callproc('remove_single_book_author_link', args)
    connection.commit()
