from models import session, Member, Book, BorrowRecord
from datetime import datetime

def list_members():
    members = session.query(Member).all()
    if members:
        print("Members:")
        for member in members:
            print(f"ID: {member.id}, Name: {member.name}")
    else:
        print("No members were found.")

def add_member(name):
    if session.query(Member).filter_by(name=name).first():
        print(f"Member {name} already exists.")
        return
    member = Member(name=name)
    session.add(member)
    session.commit()
    print(f"Added member: {name}")

def remove_member(name):
    member = session.query(Member).filter_by(name=name).first()
    if member:
        session.query(BorrowRecord).filter_by(member_id=member.id).delete()
        session.delete(member)
        session.commit()
        print(f"Removed member: {name}")
    else:
        print(f"No member was found with the name: {name}")

def add_book(title, author, quantity):
    book = Book(title=title, author=author, quantity=quantity)
    session.add(book)
    session.commit()
    print(f"Added book: {title} by {author}")

def remove_book(title):
    book = session.query(Book).filter_by(title=title).first()
    if book:
        session.delete(book)
        session.commit()
        print(f"Removed book: {title}")
    else:
        print(f"No book was found with the title: {title}")

def list_books():
    books = session.query(Book).all()
    if books:
        print("Books:")
        for book in books:
            availability = 'Available' if book.quantity > 0 else 'Not Available'
            print(f"ID: {book.id}, Title: {book.title}, Author: {book.author}, Quantity: {book.quantity}, Availability: {availability}")
    else:
        print("No books were found.")

def borrow_book(member_name, book_title, quantity):
    member = session.query(Member).filter_by(name=member_name).first()
    book = session.query(Book).filter(Book.title.like(f'%{book_title}%')).first()
    if member and book and book.quantity >= quantity:
        existing_record = session.query(BorrowRecord).filter_by(member_id=member.id, book_id=book.id, return_date=None).first()
        if existing_record:
            existing_record.quantity += quantity
            book.quantity -= quantity
            session.commit()
            print(f"{member_name} borrowed additional {quantity} copy(ies) of {book_title}")
        else:
            borrow_record = BorrowRecord(member=member, book=book, quantity=quantity, borrow_date=datetime.utcnow())
            book.quantity -= quantity
            session.add(borrow_record)
            session.commit()
            print(f"{member_name} borrowed {quantity} copy(ies) of {book_title}")
    else:
        print("Member or Book was not found or insufficient quantity.")

def return_book(member_name, book_title, quantity):
    member = session.query(Member).filter_by(name=member_name).first()
    book = session.query(Book).filter(Book.title.like(f'%{book_title}%')).first()
    if member and book:
        borrow_record = session.query(BorrowRecord).filter_by(member_id=member.id, book_id=book.id).first()
        if borrow_record and borrow_record.return_date is None:
            borrow_record.return_date = datetime.utcnow()
            book.quantity += quantity
            session.commit()
            print(f"{member_name} returned {quantity} copy(ies) of {book_title}")
        else:
            print("Borrow record was not found or has already been returned.")
    else:
        print("Member or Book was not found.")

def list_borrowed_books():
    records = session.query(BorrowRecord).filter(BorrowRecord.return_date.is_(None)).all()
    if records:
        print("Borrowed Books:")
        for record in records:
            print(f"Member: {record.member.name}, Book: {record.book.title}, Quantity: {record.quantity}, Borrow Date: {record.borrow_date}")
    else:
        print("No books are currently borrowed.")
