

-- Administrator: Add/Update/Delete Library Branches

DELIMITER $$
DROP PROCEDURE IF EXISTS admin_branches$$

CREATE PROCEDURE admin_branches(IN pAUD VARCHAR(1), IN pbranchId INT, pbranchName VARCHAR(45), IN pbranchAddress VARCHAR(45))
BEGIN
    DECLARE DuplicateKey CONDITION for 1062;
    DECLARE EXIT HANDLER FOR DuplicateKey
    SELECT 'Duplicate key error' as message;
	SET @branchId = (SELECT MAX(lb.branchId) + 1 FROM tbl_library_branch lb);
	IF pAUD = 'A' THEN
		INSERT INTO tbl_library_branch VALUES(@branchId, pbranchName, pbranchAddress);
    END IF;
    IF pAUD = 'U' THEN
		IF pbranchAddress <> 'N/A' AND pbranchAddress <> '' THEN
			UPDATE tbl_library_branch
			SET branchAddress = pbranchAddress
			WHERE branchId = pbranchId;
		END IF;
		IF pbranchName <> 'N/A' AND pbranchName <> '' THEN
			UPDATE tbl_library_branch
			SET branchName = pbranchName
			WHERE branchId = pbranchId;
		END IF;
	END IF;
    IF pAUD = 'D' THEN
		DELETE FROM tbl_library_branch
		WHERE branchId = pbranchId;
	END IF;
END$$
DELIMITER ;



/*
Author:		Kevin Lai
This SQL script will create Stored Procedures for:
	1) Returning a loaned book
    2) Modifying publisher information
    3) Modifying borrower information
    4) Overriding a loaned book's due date
*/
-- Return a Book:
/*
	Returning a book means deleting the loan record/row from "tbl_book_loans".
	The composite Primary Key (bookId, branchId, cardNo) must exist in "tbl_book_loans".
	If the composite Primary Key exists, delete that record/row.
    If the composite Primary Key does not exist, respond with an error message.
*/
DELIMITER $$
DROP PROCEDURE IF EXISTS Borrower_Return_Book $$

CREATE PROCEDURE Borrower_Return_Book(
	IN  param_bookId INT,
    IN  param_branchId INT,
    IN  param_cardNo INT,
    OUT param_message VARCHAR(100)
)
BEGIN
	-- Check if the book loan is valid....
	IF	EXISTS (SELECT	*
				FROM 	tbl_book_loans
				WHERE	bookId=param_bookId
					AND	branchId=param_branchId
					AND	cardNo=param_cardNo)
	THEN
		DELETE FROM		tbl_book_loans
		WHERE			bookId=param_bookId
			AND			branchId=param_branchId
			AND			cardNo=param_cardNo;
        SET param_message='Thank you for returning this book.';
	ELSE
        SET param_message='You haven''t borrowed this book, so you can''t return it.';
	END IF;
END $$
DELIMITER ;

-- Add/Update/Delete Publishers:
/*
	Modify the records/rows in 'tbl_publisher'.
    Adding a new publisher has no cascading consequences.
    Updating an existing publisher has no cascading consequences.
    Deleting an existing publisher has no cascading consequences,
		because the Foreign Key in 'tbl_book' is allowed to be NULL.
*/

DELIMITER $$
DROP PROCEDURE IF EXISTS Modify_Publisher $$

CREATE PROCEDURE Modify_Publisher(
	IN  param_operation VARCHAR(1),
    IN  param_publisherId INT,
    IN  param_NEWpublisherName VARCHAR(45),
    IN  param_NEWpublisherAddress VARCHAR(45),
    IN  param_NEWpublisherPhone VARCHAR(45),
    OUT param_message VARCHAR(100)
)
BEGIN
	-- # The table 'tbl_publisher' doesn't have an Auto-Increment Primary Key.
    -- # Therefore, we have to manually increment the Primary Key.
    DECLARE biggest_ID INT DEFAULT 0;

    SELECT	MAX(publisherId)
    INTO	biggest_ID
    FROM	tbl_publisher;

    -- # If the table is empty, then [biggest_ID] is NULL
		IF	biggest_ID IS NULL THEN
			SET biggest_ID=1;
		ELSE
			SET biggest_ID=biggest_ID+1;
		END IF;

    -- # Decide which operation to perform....
	CASE param_operation
		WHEN 'A' THEN
			INSERT INTO tbl_publisher (publisherId, publisherName, publisherAddress, publisherPhone)
            VALUES (biggest_ID, param_NEWpublisherName, param_NEWpublisherAddress, param_NEWpublisherPhone);
            SET param_message='Added the new publisher information.';
		WHEN 'U' THEN
			UPDATE	tbl_publisher
			SET		publisherName=param_NEWpublisherName,
					publisherAddress=param_NEWpublisherAddress,
                    publisherPhone=param_NEWpublisherPhone
			WHERE	publisherId=param_publisherId;
            SET param_message='Updated the old publisher information.';
		WHEN 'D' THEN
			DELETE FROM	tbl_publisher
            WHERE 		publisherId=param_publisherId;
			SET param_message='Deleted the publisher.';
		ELSE
			SET param_message='Please choose a valid operation.';
	END CASE;
END $$
DELIMITER ;


-- Add/Update/Delete Borrowers:
/*
	Modify the records/rows in 'tbl_borrower'.
    Adding a new borrower has no cascading consequences.
    Updating an existing borrower has no cascading consequences.
    Deleting an existing borrower does have cascading consequences,
		because the composite Primary Key in 'tbl_book_loans' contains 'tbl_borrower.cardNo'.
        Therefore, we must ensure that a 'tbl_borrower.cardNo' that we want to delete
        does not exist in the 'tbl_book_loans'.
	In other words, a borrower with an outstanding loan cannot be deleted.
    The borrower must return all borrowed books, before being deleted from the database.
*/

DELIMITER $$
DROP PROCEDURE IF EXISTS Modify_Borrower$$

CREATE PROCEDURE Modify_Borrower(
	IN  param_operation VARCHAR(1),
    IN  param_cardNo INT,
    IN  param_NEWname VARCHAR(45),
    IN  param_NEWaddress VARCHAR(45),
	IN  param_NEWphone varchar(45),
    OUT param_message VARCHAR(100)
)
BEGIN
	-- # The table 'tbl_borrower' doesn't have an Auto-Increment Primary Key.
    -- # Therefore, we have to manually increment the Primary Key.
    DECLARE biggest_ID INT DEFAULT 0;

    SELECT	MAX(cardNo)
    INTO	biggest_ID
    FROM	tbl_borrower;

    -- # If the table is empty, then [biggest_ID] is NULL
		IF	biggest_ID IS NULL THEN
			SET biggest_ID=1;
		ELSE
			SET biggest_ID=biggest_ID+1;
		END IF;

    -- # Decide which operation to perform....
	CASE param_operation
		WHEN 'A' THEN
			INSERT INTO tbl_borrower (cardNo, name, address, phone)
            VALUES (biggest_ID, param_NEWname, param_NEWaddress, param_NEWphone);
            SET param_message='Added the new borrower information.';
		WHEN 'U' THEN
			UPDATE	tbl_borrower
			SET		name=param_NEWname,
					address=param_NEWaddress,
					phone=param_NEWphone
			WHERE	cardNo=param_cardNo;
            SET param_message='Updated the old borrower information.';
		WHEN 'D' THEN
			IF	NOT EXISTS (SELECT	*
							FROM 	tbl_book_loans
							WHERE	cardNo=param_cardNo)
			THEN	-- the borrower has no existing loans, and can be deleted
				DELETE FROM		tbl_borrower
				WHERE			cardNo=param_cardNo;
				SET param_message='Deleted the borrower.';
			ELSE
				SET param_message='Borrower has existing loans.  Cannot delete the borrower.';
			END IF;
		ELSE
			SET param_message='Please choose a valid operation.';
	END CASE;
END $$
DELIMITER ;


-- # Override Due Date for a Book Loan:
/*
	Modify the due date for an existing book loan.
    Check that the book loan exists, then update the due date.
*/
DELIMITER $$
DROP PROCEDURE IF EXISTS Change_DueDate $$

CREATE PROCEDURE Change_DueDate(
	IN  param_bookId INT,
    IN	param_branchId INT,
    IN  param_cardNo INT,
    IN	param_NEWdate DATETIME,
    OUT param_message VARCHAR(100)
)
BEGIN
	UPDATE	tbl_book_loans
	SET		dueDate=param_NEWdate
	WHERE	bookId=param_bookId
		AND	branchId=param_branchId
        AND	cardNo=param_cardNo;
    SET param_message='New due date has been assigned.';
END $$
DELIMITER ;


/*wrapper function for Kevin's Return Book, to expose return string to python*/

/*################################################*/
delimiter $$

drop function if exists Borrower_Return_Book_test_proc$$

create function Borrower_Return_Book_test_proc(
bkID int,
branchID int,
cardNo int
) returns varchar(100)
deterministic
begin
declare testStr varchar(100);
call Borrower_Return_Book(bkID, branchID, cardNo, testStr);
return testStr;
end$$

delimiter ;

/*
select Borrower_Return_Book_test_proc(2, 1, 111);
*/
/*################################################*/

/*################################################*/
delimiter $$

drop function if exists Admin_Modify_Publisher$$

create function Admin_Modify_Publisher(
p_op varchar(1),
pubID int,
newName varchar(45),
newAddress varchar(45),
newPhone varchar(45)
)
returns varchar(100)
deterministic
begin
declare testStr varchar(100) default '';
call Modify_Publisher(p_op, pubID, newName, newAddress, newPhone, testStr);
return testStr;
end$$

delimiter ;

/*################################################*/

/*################################################*/
delimiter $$

drop function if exists Admin_Override_Due_Date$$

create function Admin_Override_Due_Date(
param_bookId INT,
param_branchId INT,
param_cardNo INT,
param_NEWdate DATETIME
)
returns varchar(100)
deterministic
begin
declare testStr varchar(100) default '';
call Change_DueDate(param_bookId, param_branchId, param_cardNo, param_NEWdate, testStr);
return testStr;
end$$

delimiter ;

/*################################################*/


delimiter $$

drop procedure if exists get_books_by_branch_id$$

create procedure get_books_by_branch_id(in brID int)
begin
select tbook.bookId, tbook.title
from tbl_book tbook, tbl_book_copies tcopies, tbl_library_branch tbranch
where tbook.bookId=tcopies.bookId
and tcopies.branchId=tbranch.branchId
and tbranch.branchId=brID;
end $$

delimiter ;


delimiter $$

drop procedure if exists get_books_by_branch_name$$

create procedure get_books_by_branch_name(in brName VARCHAR(45))
begin
select tbook.bookId, tbook.title
from tbl_book tbook, tbl_book_copies tcopies, tbl_library_branch tbranch
where tbook.bookId=tcopies.bookId
and tcopies.branchId=tbranch.branchId
and tbranch.branchName like brName;
end $$

delimiter ;


delimiter $$

drop procedure if exists get_authors_by_book$$

create procedure get_authors_by_book(in bkId int)
begin
select tauth.authorName
from tbl_book tbook, tbl_book_authors tars, tbl_author tauth
where tbook.bookId=tars.bookId
and tars.authorId=tauth.authorId
and tbook.bookId=bkId;
end $$

delimiter ;


delimiter $$

drop procedure if exists get_num_copies$$

create procedure get_num_copies(in brId int, in bkId int)
begin
select tcopies.noOfCopies
from tbl_book tbook, tbl_book_copies tcopies, tbl_library_branch tbranch
where tbook.bookId=tcopies.bookId
and tcopies.branchId=tbranch.branchId
and tbook.bookId=bkId
and tbranch.branchId=brId;
end $$

delimiter ;

delimiter $$

drop procedure if exists get_num_books_on_loan$$

create procedure get_num_books_on_loan(in brId int, in bkId int)
begin
	select count(*)
	from tbl_book_loans
	where tbl_book_loans.branchId=brId
	and tbl_book_loans.bookId=bkId;
end$$

delimiter ;


/*
	Admin function definitions and test calls, after running all three,
    should cancel out and yield an unchanged database.
    read further below for details of each.
*/


/*
Add book by strings; first the book, then the author.
Input strings are limited to 45 characters, as per restraints of the data model.
Can only input one pair at a time.
So, if book has multiple authors, then multiple calls are required.
checks for duplicates are taken care of within function,
simply repeat your calls with the same book title and different authors.

inserts into the book, author, and book_authors tables appropriately
*/

delimiter $$

drop procedure if exists admin_add_book_and_author$$

create procedure admin_add_book_and_author(in bTitle varchar(45), in aName varchar(45))
proc_label: begin
declare newBkId int;
declare newAuthId int;
declare bookEmpty bool;
declare authEmpty bool;

set bookEmpty = not exists (select null from tbl_book);
set authEmpty = not exists (select null from tbl_author);

if bookEmpty then
	if authEmpty then
		insert into tbl_book(bookId, title) values (1, bTitle);
        insert into tbl_author values (1, aName);
        insert into tbl_book_authors values (1, 1);
        leave proc_label;
    else
		set newBkId := 1;
	end if;
else
	if not exists (select null from tbl_book where bTitle like tbl_book.title) then
		set newBkId := (select max(tbl_book.bookId) from tbl_book)+1;
		insert into tbl_book(bookId, title) values (newBkId, bTitle);
	else
		set newBkId := (select bookId from tbl_book where bTitle like title limit 1);
	end if;
end if;



if authEmpty then
	set newAuthId := 1;
else
	if not exists (select null from tbl_author where aName like authorName) then
		set newAuthId := (select max(tbl_author.authorId) from tbl_author)+1;
		insert into tbl_author(authorId, authorName) values (newAuthId, aName);
	else
		set newAuthId := (select authorId from tbl_author where aName like tbl_author.authorName limit 1);
	end if;
end if;

insert into tbl_book_authors values (newBkId, newAuthId);
end $$

delimiter ;



/*
admin update has a complicated parameter list;

first- book ID to be used as a look-up reference
second- Author ID for same
third- String containing the new title(limited to 45 chars)
fourth- int specifying the new foreign key linking the publisher table
fifth- String containing new author name(same 45 char limit)
*/

delimiter $$

drop procedure if exists admin_update_book_and_author$$

create procedure admin_update_book_and_author(
	in bkID int, in authID int, in newTitle varchar(45), in newPubID int, in newAuthName varchar(45)
)
begin
update tbl_book set title=newTitle, pubId=newPubID where bkID=bookId;
update tbl_author set authorName=newAuthName where authID=authorId;
end$$

delimiter ;



/*
deletes single row from each of the book, author, and book_authors tables according to parameter;
first- integer book ID
*/

delimiter $$

drop procedure if exists admin_delete_book_and_author$$

create procedure admin_delete_book_and_author(in bkID int)
begin
	declare done int default 0;
    declare current_aid int;
    declare aidCurs cursor for select authorId from tbl_book_authors where bookId=bkID;
    declare continue handler for not found set done=1;

    open aidCurs;

    repeat
		fetch aidCurs into current_aid;
        delete from tbl_book_authors where bookId=bkID and authorId=current_aid;
		if not exists (select null from tbl_book_authors where authorId=current_aid) then
			delete from tbl_author where authorId=current_aid;
        end if;
    until done
    end repeat;

	close aidCurs;

	delete from tbl_book where bookId=bkID;
end$$

delimiter ;



-- ****************************************************************************
/*
Procedure 1: Give a list of Library branches using the names or locations like this:
*/
delimiter $$

DROP PROCEDURE IF EXISTS getBranches$$

CREATE PROCEDURE getBranches()
BEGIN
    SELECT branchName, branchId, branchAddress
    FROM tbl_library_branch;
END$$

delimiter ;

/*
Procedure 5: Update num copies
*/
delimiter $$

DROP PROCEDURE IF EXISTS updateNoOfCopies$$

CREATE PROCEDURE updateNoOfCopies(in bkID int, in brID int, in newNoCopies int)
BEGIN
    UPDATE tbl_book_copies
    SET noOfCopies = newNoCopies
    WHERE tbl_book_copies.bookId=bkID
    AND tbl_book_copies.branchId=brID;
END$$

delimiter ;

/*
Procedure NA: Add to tbl_copies
*/
delimiter $$

DROP PROCEDURE IF EXISTS add_to_tbl_copies$$

CREATE PROCEDURE add_to_tbl_copies(in bkID int, in brID int, in newNoCopies int)
BEGIN
    INSERT INTO tbl_book_copies (bookId, branchId, noOfCopies)
    VALUES (bkID, brID, newNoCopies);
END$$

delimiter ;

/*
Procedure NA: Get book Id from author name and book title
*/
delimiter $$

DROP PROCEDURE IF EXISTS get_book_from_author_title$$

CREATE PROCEDURE get_book_from_author_title(in author_name varchar(45), in book_title varchar(45))
BEGIN
    SELECT tbl_book_authors.bookId FROM tbl_book_authors
	INNER JOIN tbl_author 
	ON tbl_author.authorId=tbl_book_authors.authorId 
	INNER JOIN tbl_book 
	ON tbl_book.bookId=tbl_book_authors.bookId
	WHERE tbl_author.authorName=author_name
	AND tbl_book.title=book_title;
END$$

delimiter ;

/*
Procedure NA: get all books
*/
delimiter $$

DROP PROCEDURE IF EXISTS getAllBooks$$

CREATE PROCEDURE getAllBooks()
BEGIN
    SELECT * FROM tbl_book;
END$$

delimiter ;

/*
Procedure NA: get all publishers
*/
delimiter $$

DROP PROCEDURE IF EXISTS get_all_publishers$$

CREATE PROCEDURE get_all_publishers()
BEGIN
    SELECT * FROM tbl_publisher;
END$$

delimiter ;


/*
Procedure NA: get authors ids from book
*/
delimiter $$

DROP PROCEDURE IF EXISTS get_authors_from_book$$

CREATE PROCEDURE get_authors_from_book(in bkID int)
BEGIN
    SELECT tbl_book_authors.authorId, tbl_author.authorName
    FROM tbl_book_authors, tbl_author
    WHERE tbl_book_authors.bookId=bkID
    AND tbl_book_authors.authorId=tbl_author.authorId;
END$$

delimiter ;


/*
Procedure 8: checkout book
*/
DELIMITER $$

drop procedure if exists checkout_book$$

CREATE PROCEDURE checkout_book(
    in bkID int, in brID int, in cNo int
)
BEGIN
    INSERT INTO tbl_book_loans (
        bookId, branchId, cardNo, dateOut, dueDate
    ) VALUES (
        bkID, brID, cNo, NOW(), DATE_ADD(NOW(), INTERVAL 7 DAY)
    );
END$$

DELIMITER ;

-- Borrower: books due by card no
DELIMITER $$
DROP PROCEDURE IF EXISTS get_books_due$$

CREATE PROCEDURE get_books_due(IN pcardNo INT)
BEGIN
SELECT bl.bookId, b.title
FROM tbl_book_loans bl, tbl_book b
WHERE bl.bookId = b.bookId AND cardNo = pcardNo;
END;
$$
DELIMITER ;

-- Borrower: check valid card number
delimiter $$
drop procedure if exists card_number_exists$$

CREATE PROCEDURE card_number_exists(IN pcardNo INT)
BEGIN
  SELECT cardNo
  FROM tbl_borrower
  WHERE cardNo = pcardNo;
END;
$$
delimiter ;




-- get borrower
delimiter $$

drop procedure if exists get_borrower$$

CREATE PROCEDURE get_borrower(IN cNo INT)
BEGIN
	SELECT *
	FROM tbl_borrower
	WHERE tbl_borrower.cardNo=cNo;
END$$

delimiter ;


-- check if existing loans for borrower exists


delimiter $$

drop procedure if exists check_existing_loans$$

CREATE PROCEDURE check_existing_loans(IN cNo INT)
BEGIN
	SELECT	*
	FROM tbl_book_loans
	WHERE cardNo=cNo;
END$$

delimiter ;


/*checks for pre-existing loan in case of duplicate check-out attempts*/

delimiter $$

drop function if exists duplicate_loan_check$$

create function duplicate_loan_check(bkID int, brID int, cardN int)
returns bool
deterministic
begin
	if exists (select null from tbl_book_loans where bookId=bkID and branchId=brID and cardNo=cardN) then
		return true;
    else
		return false;
    end if;
end$$

delimiter ;


delimiter $$

drop procedure if exists remove_single_book_author_link$$

create procedure remove_single_book_author_link(in bkID int, in authID int)
begin

if (select count(authorId) from tbl_book_authors where bookId=bkID)>1 then
	delete from tbl_book_authors where bookId=bkID and authorId=authId;
end if;
if not exists (select null from tbl_book_authors where authorId=authId) then
	delete from tbl_author where authorId=authId;
end if;


end$$

delimiter ;

