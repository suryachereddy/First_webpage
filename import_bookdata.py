import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://rljdkhwyibrclr:83b8058cc1429ab991e99a6bdf0f137575a6a87654989daa21d4cce4891134fc@ec2-50-17-90-177.compute-1.amazonaws.com:5432/d2adq2pnnb6dg2")
#engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn, title, author, year in reader:
        db.execute("INSERT INTO test (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added data, book_title: {title}")
    db.commit()

if __name__ == "__main__":
    main()
