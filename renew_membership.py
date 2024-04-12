import cx_Oracle
from datetime import datetime, timedelta

def renew_membership(connection, card_id):
    cursor = connection.cursor()

    cursor.execute("""
        SELECT EXPIRY_DATE FROM MEMBER WHERE CARD_ID = :card_id
    """, card_id=card_id)
    current_expiry_date = cursor.fetchone()[0]

    new_expiry_date = current_expiry_date + timedelta(days=365)

    cursor.execute("""
        UPDATE MEMBER SET EXPIRY_DATE = :new_expiry_date 
        WHERE CARD_ID = :card_id
    """, new_expiry_date=new_expiry_date, card_id=card_id)

    connection.commit()
    cursor.close()

    cursor = connection.cursor()
    cursor.execute("""
        SELECT EXPIRY_DATE FROM MEMBER WHERE CARD_ID = :card_id
    """, card_id=card_id)
    updated_expiry_date = cursor.fetchone()[0]

    if updated_expiry_date > current_expiry_date:
        print("Membership successfully extended.")
    else:
        print("Membership extension failed.")

    cursor.close()

if __name__ == "__main__":
    connection = cx_Oracle.connect(user='yxn5384', password='Yagnavarsha731', dsn='az6F72ldbp1.az.uta.edu:1523/pcse1p.data.uta.edu')

    card_id = input("Enter Card ID for membership renewal: ")

    renew_membership(connection, card_id)
