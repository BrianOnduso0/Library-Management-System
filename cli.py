import click
from datetime import datetime
from models import session, Member, Book, BorrowRecord, init_db

@click.group()
def cli():
    pass

@click.command()
def init():
    """Initialize the database."""
    init_db()
    click.echo("Initialized the database.")

@click.command()
@click.argument('name')
def add_member(name):
    """Add a new member."""
    member = Member(name=name)
    session.add(member)
    session.commit()
    click.echo(f"Added member: {name}")

@click.command()
@click.argument('name')
def remove_member(name):
    """Remove a member."""
    member = session.query(Member).filter_by(name=name).first()
    if member:
        session.delete(member)
        session.commit()
        click.echo(f"Removed member: {name}")
    else:
        click.echo(f"No member found with name: {name}")

@click.command()
def list_members():
    """List all members."""
    members = session.query(Member).all()
    members_list = [(member.id, member.name) for member in members]
    if members_list:
        click.echo("Members:")
        for member in members_list:
            click.echo(f"ID: {member[0]}, Name: {member[1]}")
    else:
        click.echo("No members found.")

@click.command()
@click.argument('title')
@click.argument('author')
@click.argument('quantity', type=int)
def add_book(title, author, quantity):
    """Add a new book."""
    book = Book(title=title, author=author, quantity=quantity)
    session.add(book)
    session.commit()
    click.echo(f"Added book: {title} by {author}, Quantity: {quantity}")

@click.command()
@click.argument('title')
@click.argument('quantity', type=int)
def remove_book(title, quantity):
    """Remove books."""
    book = session.query(Book).filter_by(title=title).first()
    if book:
        if book.quantity >= quantity:
            book.quantity -= quantity
            if book.quantity == 0:
                session.delete(book)
            session.commit()
            click.echo(f"Removed {quantity} of {title}")
        else:
            click.echo(f"Cannot remove {quantity} of {title}, only {book.quantity} available")
    else:
        click.echo(f"No book found with title: {title}")

@click.command()
def list_books():
    """List all books and their availability."""
    books = session.query(Book).all()
    books_list = [(book.id, book.title, book.author, book.quantity) for book in books]
    if books_list:
        click.echo("Books:")
        for book in books_list:
            availability = 'Available' if book[3] > 0 else 'Not Available'
            click.echo(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Quantity: {book[3]}, Availability: {availability}")
    else:
        click.echo("No books found.")

@click.command()
@click.argument('member_name')
@click.argument('book_title')
@click.argument('quantity', type=int)
def borrow_book(member_name, book_title, quantity):
    """Record a book borrowing."""
    member = session.query(Member).filter_by(name=member_name).first()
    book = session.query(Book).filter_by(title=book_title).first()
    if member and book and book.quantity >= quantity:
        borrow_record = BorrowRecord(member=member, book=book)
        book.quantity -= quantity
        session.add(borrow_record)
        session.commit()
        click.echo(f"{member_name} borrowed {quantity} copy of {book_title} Book")
    else:
        click.echo("A Member or the Book selected was not found,not enough books are available. Please choose the correct details.")

@click.command()
@click.argument('member_name')
@click.argument('book_title')
@click.argument('quantity', type=int)
def return_book(member_name, book_title, quantity):
    """Record a book return."""
    member = session.query(Member).filter_by(name=member_name).first()
    book = session.query(Book).filter_by(title=book_title).first()
    if member and book:
        borrow_record = session.query(BorrowRecord).filter_by(member_id=member.id, book_id=book.id).first()
        if borrow_record and borrow_record.return_date is None:
            borrow_record.return_date = datetime.utcnow()
            book.quantity += quantity
            session.commit()
            click.echo(f"{member_name} returned {quantity} of {book_title} book")
        else:
            click.echo("The Borrow record was not found or the book was already returned.")
    else:
        click.echo("The Member or Book was not found. Please choose the correct details")

@click.command()
def list_borrowed_books():
    """List all borrowed books."""
    records = session.query(BorrowRecord).filter(BorrowRecord.return_date.is_(None)).all()
    borrowed_books = [
        {
            "member_name": record.member.name,
            "book_title": record.book.title,
            "borrow_date": record.borrow_date
        }
        for record in records
    ]
    if borrowed_books:
        click.echo("Borrowed Books:")
        for record in borrowed_books:
            click.echo(f"Member: {record['member_name']}, Book: {record['book_title']}, Borrow Date: {record['borrow_date']}")
    else:
        click.echo("No books have been currently borrowed.")

cli.add_command(init)
cli.add_command(add_member)
cli.add_command(remove_member)
cli.add_command(list_members)
cli.add_command(add_book)
cli.add_command(remove_book)
cli.add_command(list_books)
cli.add_command(borrow_book)
cli.add_command(return_book)
cli.add_command(list_borrowed_books)

if __name__ == '__main__':
    cli()
