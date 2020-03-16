import procedures
import constants

class Book:
    def __init__(self, bookId=None, title=None, pubId=None, cursor=None):
        self.bookId = bookId
        self.title  = title
        self.pubId  = pubId
        self.authors = []
        self.cursor = cursor        

    def __str__(self):
        self.get_authors_by_book()
        book_info = []
        book_list_item = self.title
        i = 0
        for author in self.authors:
            if i == 0:
                book_list_item += ' by '
            elif i < len(self.authors):
                book_list_item += ' and '
            book_list_item += author
            i += 1
        return constants.bcolor.get_color('blue', book_list_item)

    def get_authors_by_book(self):
        args = (self.bookId,)
        self.cursor.callproc('get_authors_from_book', args)
        authors_dictionary = {}
        i = 1
        for result in self.cursor.stored_results():
            authors = result.fetchall()
            for author in authors:
                authors_dictionary[i] = [author[0], author[1]]
                self.authors.append(author[1])
                i += 1
        return authors_dictionary

    def get_num_copies(self, branchId):
        args = (branchId, self.bookId,)
        self.cursor.callproc('get_num_copies', args)
        number_of_copies = 0
        for result in self.cursor.stored_results():
            num_copies = result.fetchall()
            for num in num_copies:
                number_of_copies = num[0]
        return number_of_copies

    def update_num_of_copies(self, connection, branchId, newNumOfCopies):
        args = (self.bookId, branchId, newNumOfCopies,)
        self.cursor.callproc('updateNoOfCopies', args)
        connection.commit()

class BookLoan:
    def __init__(self, bookId, branchId, cardNo, dateOut=None, dueDate=None):
        self.bookId   = bookId
        self.branchId = branchId
        self.cardNo   = cardNo
        self.dateOut  = dateOut
        self.dueDate  = dueDate

    def change_DueDate(self, cursor, connection, newDate):
        cursor.execute('select Admin_Override_Due_Date(%s, %s, %s, %s)', (self.bookId, self.branchId, self.cardNo, newDate))
        rows = cursor.fetchall()
        results = len(rows)
        ret = ''
        if results > 0:
            row = rows[0]
            ret = row[0]

        connection.commit()
        return ret

class Branch:
    def __init__(self, branchId=None, branchName=None, branchAddress=None):
        self.branchId      = branchId
        self.branchName    = branchName
        self.branchAddress = branchAddress

    def __str__(self):
        return_str = '{}, {}'.format(self.branchName, self.branchAddress)
        return constants.bcolor.get_color('blue', return_str)

    def add_branch(self, cursor, connection):
        action = 'A'
        branchId = 0 # updated in MySQL stored procedure.
        args = (action, branchId, self.branchName, self.branchAddress,)
        cursor.callproc('admin_branches', args)
        connection.commit()

    def update_branch(self, cursor, connection):
        action = 'U'
        args = (action, self.branchId, self.branchName, self.branchAddress,)
        cursor.callproc('admin_branches', args)
        connection.commit()

    def delete_branch(self, cursor, connection):
        action = 'D'
        args = (action, self.branchId, '', '',)
        cursor.callproc('admin_branches', args)
        connection.commit()
        return True
    
    def get_books_by_branch_id(self, cursor):
        args = (self.branchId,)
        cursor.callproc('get_books_by_branch_id', args)
        book_list = []
        for result in cursor.stored_results():
            books = result.fetchall()
            for book in books:
                book_list.append(Book(book[0], book[1], None, cursor))
        return book_list

class Publisher:
    def __init__(self, publisherId, publisherName, publisherAddress, publisherPhone):
        self.publisherId      = publisherId
        self.publisherName    = publisherName
        self.publisherAddress = publisherAddress
        self.publisherPhone   = publisherPhone

    def __str__(self):
        return self.publisherName

    def modify_publisher(self, cursor, connection, param_operation):
        cursor.execute('select Admin_Modify_Publisher(%s, %s, %s, %s, %s)', (param_operation, self.publisherId, self.publisherName, self.publisherAddress, self.publisherPhone))
        rows = cursor.fetchall()
        results = len(rows)
        ret = ''
        if results > 0:
            row = rows[0]
            ret = row[0]
        connection.commit()
        return ret