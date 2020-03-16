from procedures import sql_connect, sql_close
import constants
from librarian import Librarian 
from administrator import Administrator
from borrower import Borrower

def entryPrompt():
    print(constants.MENU_LINE_BREAK)
    print(constants.WELCOME_MESSAGE)
    print(constants.LINE_BREAK)
    print(constants.USER_TYPES)
    print(constants.LINE_BREAK)

    user_type = input(constants.MAKE_SELECTION)
    if user_type.isdigit():
        return int(user_type)
    
    return user_type

def main():
    # connect to database
    connection = sql_connect()
    cnx = connection[0]
    cursor = connection[1]

    USER_TYPES = {
        1: Librarian(cursor, cnx),
        2: Administrator(cursor, cnx),
        3: Borrower(cursor, cnx),
    }

    while True:
        user_type = entryPrompt()
        if user_type == 'quit':
            print(constants.QUIT_MESSAGE)
            break
        func = USER_TYPES.get(user_type)
        if not func:
            print(constants.INCORRECT_INPUT)
        else:
            continue_driver = func.driver()
            if not continue_driver:
                print(constants.QUIT_MESSAGE)
                break

    # close cursor and connection
    sql_close(cnx, cursor)

main()