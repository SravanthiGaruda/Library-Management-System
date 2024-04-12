import cx_Oracle
from datetime import datetime

def new_borrow(connection, isbn, card_id, borrow_date):
    cursor = connection.cursor()

    try:
        borrow_date = datetime.strptime(borrow_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        
        cursor.execute("""
            SELECT TOTAL_COPIES, COPIES_ON_LOAN 
            FROM BOOK 
            WHERE ISBN = :isbn AND STATUS_TO_LEND = 1
        """, isbn=isbn)
        book_info = cursor.fetchone()
        
        cursor.execute("SELECT NO_OF_BOOKS_BORROWED FROM MEMBER WHERE CARD_ID = :card_id", card_id=card_id)
        books_borrowed = cursor.fetchone()[0]

        if book_info and book_info[1] < book_info[0] and books_borrowed < 5:
            cursor.execute("""
                UPDATE BOOK SET 
                COPIES_ON_LOAN = COPIES_ON_LOAN + 1, 
                BORROW_DATE = TO_DATE(:borrow_date, 'YYYY-MM-DD'), 
                CARD_ID = :card_id 
                WHERE ISBN = :isbn
            """, borrow_date=borrow_date, card_id=card_id, isbn=isbn)

            cursor.execute("INSERT INTO CAN_ACCESS (ISBN, CARD_ID) VALUES (:isbn, :card_id)", isbn=isbn, card_id=card_id)

            cursor.execute("UPDATE MEMBER SET NO_OF_BOOKS_BORROWED = NO_OF_BOOKS_BORROWED + 1 WHERE CARD_ID = :card_id", card_id=card_id)

            connection.commit()
            print("Book borrowed successfully!")
        else:
            if not book_info:
                print("Book not available for borrowing or not set to lend.")
            elif book_info[1] == book_info[0]:
                print("All copies of the book are already on loan.")
            elif books_borrowed >= 5:
                print("Member has reached the maximum number of books allowed for borrowing.")

    except ValueError:
        print("Please enter the date in the format YYYY-MM-DD.")

    cursor.close()

if __name__ == "__main__":
    connection = cx_Oracle.connect(user='yxn5384', password='Yagnavarsha731', dsn='az6F72ldbp1.az.uta.edu:1523/pcse1p.data.uta.edu')

    isbn = input("Enter ISBN: ")
    card_id = input("Enter Card ID: ")
    borrow_date_input = input("Enter Borrow Date (YYYY-MM-DD): ")
  
    borrow_date = borrow_date_input.strip("'\"")

    new_borrow(connection, isbn, card_id, borrow_date)
