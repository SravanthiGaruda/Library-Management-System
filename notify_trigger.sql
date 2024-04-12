CREATE OR REPLACE TRIGGER notify_overdue_book
AFTER UPDATE ON BOOK
FOR EACH ROW
WHEN (NEW.RETURN_DATE < CURRENT_DATE AND NEW.COPIES_ON_LOAN > 0)
BEGIN
    
    DBMS_OUTPUT.PUT_LINE('Attention: Overdue Book Notification');
    DBMS_OUTPUT.PUT_LINE('Dear Member, your book with ISBN ' || :NEW.ISBN || ' is overdue.');
   
END notify_overdue_book;
/


CREATE OR REPLACE TRIGGER notify_membership_renewal
BEFORE UPDATE ON MEMBER
FOR EACH ROW
WHEN (NEW.EXPIRY_DATE - SYSDATE <= 7)
BEGIN
    
    DBMS_OUTPUT.PUT_LINE('Attention: Membership Renewal Notification');
    DBMS_OUTPUT.PUT_LINE('Dear Member, your membership is expiring soon. Please renew to continue using our services.');
   
END notify_membership_renewal;
/