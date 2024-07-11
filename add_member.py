import cx_Oracle
from datetime import datetime, timedelta

def add_member(connection, card_id, no_of_books_borrowed, email, issue_date, expiry_date):
    cursor = connection.cursor()
    
    if not expiry_date:
        expiry_date = (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d')  
    issue_date = datetime.strptime(issue_date, '%Y-%m-%d')

    cursor.execute("""
        INSERT INTO MEMBER (CARD_ID, NO_OF_BOOKS_BORROWED, EMAIL, ISSUE_DATE, EXPIRY_DATE)
        VALUES (:card_id, :no_of_books_borrowed, :email, TO_DATE(:issue_date, 'YYYY-MM-DD'), TO_DATE(:expiry_date, 'YYYY-MM-DD'))
    """, card_id=card_id, no_of_books_borrowed=no_of_books_borrowed, email=email, issue_date=issue_date.strftime('%Y-%m-%d'), expiry_date=expiry_date)
    connection.commit()
    cursor.close()
    
    print("Member with Card ID: {} has been successfully added.".format(card_id))

connection = cx_Oracle.connect(user='', password='', dsn='')

card_id = int(input("Enter Card ID: "))
no_of_books_borrowed = int(input("Enter Number of Books Borrowed: "))
email = input("Enter Email: ")
issue_date = input("Enter Issue Date (YYYY-MM-DD): ")
expiry_date = input("Enter Expiry Date (YYYY-MM-DD): ")

add_member(connection, card_id, no_of_books_borrowed, email, issue_date, expiry_date)
