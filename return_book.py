import cx_Oracle
from datetime import datetime

def return_book(connection, isbn, card_id, return_date):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT TITLE, BORROW_DATE, RETURN_DATE 
        FROM BOOK 
        WHERE ISBN = :isbn AND CARD_ID = :card_id
    """, isbn=isbn, card_id=card_id)
    book_info = cursor.fetchone()

    if book_info:
        title, borrow_date, actual_return_date = book_info
        days_borrowed = None
        fine = 0
        
        if actual_return_date:  
            days_borrowed = (actual_return_date - borrow_date).days
            if days_borrowed > 21 and not is_professor(card_id):  
                fine = (days_borrowed - 21) * 0.5
            elif days_borrowed > 90:  
                fine = 0

       
        cursor.execute("""
            UPDATE BOOK SET COPIES_ON_LOAN = COPIES_ON_LOAN - 1, 
            RETURN_DATE = TO_DATE(:return_date, 'YYYY-MM-DD'), 
            CARD_ID = NULL 
            WHERE ISBN = :isbn AND CARD_ID = :card_id
        """, isbn=isbn, card_id=card_id, return_date=return_date)

    
        cursor.execute("""
            UPDATE MEMBER SET NO_OF_BOOKS_BORROWED = NO_OF_BOOKS_BORROWED - 1 
            WHERE CARD_ID = :card_id
        """, card_id=card_id)

        connection.commit()
        cursor.close()

       
        print("Return Receipt")
        print("--------------")
        print("Book Title: {}".format(title))
        print("Days Borrowed: {}".format(days_borrowed if days_borrowed is not None else "Not available"))
        print("Borrowed Date: {}".format(borrow_date))
        print("Returned Date: {}".format(return_date))
        print("Fine: ${}".format(fine))
        print("--------------")
    else:
        cursor.close()
        print("Book not found or not borrowed by the member.")

def is_professor(card_id):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM PROFESSOR WHERE CARD_ID = :card_id", card_id=card_id)
    result = cursor.fetchone()
    cursor.close()
    return result is not None

if __name__ == "__main__":
    isbn = input("Enter ISBN: ")
    card_id = input("Enter Card ID: ")
    return_date = input("Enter Return Date (YYYY-MM-DD): ")

    connection = cx_Oracle.connect(user='', password='', dsn='')
    return_book(connection, isbn, card_id, return_date)
