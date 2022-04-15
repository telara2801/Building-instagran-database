import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import exists 
from eralchemy import render_er

database = declarative_base()
db = SQLAlchemy()

class Base(db.Model):
    __abstract__=True
    created=db.Column(db.DateTime(timezone=True), default=db.func.now())
    updated=db.Column(db.DateTime(timezone=True), default=db.func.now(), onupdate=db.func.now())

        
        

    def __init__(self, **kwargs): # keyword arguments
        """
        kwargs = {
        "name": "Luke",
        "eye_color": "brown",
        ...
        }
        """
        for (key, value) in kwargs.items(): #
            if key in ('created', 'updated'): continue
            if hasattr(self, key): #
                attribute_type = getattr(self.__class__, key).type
                try:
                    attribute_type.python_type(value)
                    setattr(self, key, value)
                except Exception as error:
                    print("ignoring key ", key, " with ", value, " for ", attribute_type.python_type, " because ", error.args)

    @classmethod
    def create(cls, **data):
        # crear la instancia
        instance = cls(**data)
        if (not isinstance(instance, cls)):
            print("FALLA EL CONSTRUCTOR")
            return None
        # guardar en bdd
        db.session.add(instance)
        try:
            ##Cambio de tulio es el existe valiadtion
            db.session.commit()
            print(f"created: {instance.id}")
            return instance
        except Exception as error:
            db.session.rollback()
            #return jsonify({"msg":f"The id alreade exist in database{User.id}, please add another id"})
            raise Exception(error.args)    

 

class User(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email=Column(String(20))
    posts = relationship("Post", backref="user")

    def __repr__(self):
        return f" {self.id},{self.name}, {self.email}"
    

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


class Post(Base):
    id = Column(Integer, primary_key=True)
    type_post = Column(String(100))
    total_likes = Column(String(250))
    total_comments= Column(String(250)) 
    user_id = Column(Integer, ForeignKey('user.id'))
    postComments = relationship("Post_comments", backref="post")
    postLikes= relationship("Post_likes", backref="post")

    def __repr__(self):
        return f" {self.id},{self.type_post}, {self.total_likes}"
    

    def serialize(self):
        return {
            "id": self.id,
            "type_post": self.type_post,
            "total_likes": self.total_likes,
            "total_comments": self.total_comments
        }


class User_feeds(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
    
    

    def __repr__(self):
        return f" {self.id}"
    

    def serialize(self):
        return {
            "id": self.id,
            "type_post": self.type_post,
            "total_likes": self.total_likes,
            "total_comments": self.total_comments
        }

class Userfollower(Base):
    id = Column(Integer, primary_key=True)
    follower_id= Column(Integer, ForeignKey('userfollower.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    def __repr__(self):
        return f" {self.id},{self.follower_id}, {self.user_id}"
    

    def serialize(self):
        return {
            "id": self.id,
            "follower_id": self.follower_id,
            "user_id": self.user_id        }

class Post_comments(Base):
    id = Column(Integer, primary_key=True)
    post_id = Column(String(100))
    user_id = Column(String(250))
    comments= Column(String(250)) 
    post_id = Column(Integer, ForeignKey('post.id'))

    def __repr__(self):
        return f" {self.id},{self.comments}, {self.user_id}"
    

    def serialize(self):
        return {
            "id": self.id,
            "Post_id": self.post_id,
            "user_id": self.user_id,
            "comments": self.comments
        }
class Post_likes(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    post_id = Column(Integer, ForeignKey('post.id'))
   
    def __repr__(self):
        return f" {self.id}, {self.user_id}"
    

    def serialize(self):
        return {
            "id": self.id,
            "Post_id": self.post_id,
            "user_id": self.user_id
           
        }


#
## Draw from SQLAlchemy base
try:
    result = render_er(Base, 'diagram.png')
    print("Success! Check the diagram.png file")
except Exception as e:
    print("There was a problem genering the diagram")
    raise e