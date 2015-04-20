#!/usr/bin/python3
'''
@author: wdpypere
'''
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    title = Column(String(50))
    isbn = Column(String(50))
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", backref=backref('books', order_by=id))
    
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
            self.name, self.fullname, self.password)

class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    sirname = Column(String(50))
    
#class State(Base):
#    __tablename__ = 'states'
    
#class Change(Base):
#    __tablename__ = 'changes'
    
#class Comment(Base):
#    __tablename__ = 'comments'

#        self.author = author
#        self.read = read
#        self.comment = comment
#        self.state = state
