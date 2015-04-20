#!/usr/bin/python3
'''
@author: wdpypere
'''
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
BASE = declarative_base()


class Book(BASE):
    """
    class describing books.
    """
    __tablename__ = 'books'

    idx = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    title = Column(String(50))
    isbn = Column(String(50))
    author_id = Column(Integer, ForeignKey('authors.idx'))
    author = relationship("Author", backref=backref('books', order_by=idx))

    def __repr__(self):
        return "<User(id='%s',title='%s', isbn='%s', author='%s')>" % (
            self.idx, self.title, self.isbn, self.author)


class Author(BASE):
    """
    class describing authors.
    """
    __tablename__ = 'authors'
    idx = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    sirname = Column(String(50))

    def __repr__(self):
        pass
# class State(BASE):
#     __tablename__ = 'states'

# class Change(BASE):
#     __tablename__ = 'changes'

# class Comment(BASE):
#     __tablename__ = 'comments'

#         self.author = author
#         self.read = read
#         self.comment = comment
#        self.state = state
