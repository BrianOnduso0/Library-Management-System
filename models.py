from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

DATABASE_URI = 'sqlite:///library.db'
Base = declarative_base()
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()

class Member(Base):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    borrow_records = relationship('BorrowRecord', back_populates='member')

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    quantity = Column(Integer, default=1)
    borrow_records = relationship('BorrowRecord', back_populates='book')

class BorrowRecord(Base):
    __tablename__ = 'borrow_records'
    member_id = Column(Integer, ForeignKey('members.id'), primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
    quantity = Column(Integer, nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    member = relationship('Member', back_populates='borrow_records')
    book = relationship('Book', back_populates='borrow_records')

def init_db():
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    init_db()
