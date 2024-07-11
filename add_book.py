import cx_Oracle
from datetime import datetime

def add_book(connection, isbn, title, author, description, subject_area, total_copies):
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO BOOK (ISBN, TITLE, AUTHOR, DESCRIPTION, SUBJECT_AREA, TOTAL_COPIES)
        VALUES (:isbn, :title, :author, :description, :subject_area, :total_copies)
    """, isbn=isbn, title=title, author=author, description=description, subject_area=subject_area, total_copies=total_copies)
    connection.commit()
    cursor.close()

if __name__ == "__main__":
    connection = cx_Oracle.connect(user='', password='', dsn='')

    isbn = input("Enter ISBN: ")
    title = input("Enter Title: ")
    author = input("Enter Author: ")
    description = input("Enter Description: ")
    subject_area = input("Enter Subject Area: ")
    total_copies = input("Enter Total Copies: ")

    add_book(connection, isbn, title, author, description, subject_area, total_copies)
    print("Book '{}' (ISBN: {}) has been successfully added to the library!".format(title, isbn))
