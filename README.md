## Library Management System

This is a simple library management system developed using Python and SQLite. It allows the admins and users to perform various tasks like adding and removing members from the system by Admins Only, adding and removing books from the system by Admins only , borrowing books and returning of books by users or members whereby the availability of a book in the system is clearly defined. It also provides a report of all borrowed books with details

## Features
-Listing all members a feature available for Administrators.
-Add and Remove members from the library system.
-Add and Remove books from the library inventory.
-List all the books available in the library inventory.
-Borrowing of books by members.
-Return borrowed books to the library.
-View available books in the library.

## Prerequisites
-Python
-SQLite
-Click

## Database
-The system uses an SQLite database to store information about books, members, and borrow records. The database file is named library.db.
## To initiate the databe run command: python cli.py init   
## To add a user or member run command: python cli.py add-member "Ryan Onchwari"
## To remove a user or member run command: python cli.py remove-member "Ryan Onchwari"
## To list all members run the command: python cli.py list-members 
## To  add a new book run the command: python cli.py add-book "Python Programming" "Moringa School" 10
## To remove a book from the system run the command: python cli.py remove-book "Python Programming" 2 

## Installation
Clone the repository to your local machine:

-git clone git@github.com:BrianOnduso0/Library-Management-System.git

## Navigate to the project directory depending on your path
-use pwd to check which path the project is in after cloning

## Install the required dependencies:

-pip install -r requirements.txt

## Run the application:

-python main.py
