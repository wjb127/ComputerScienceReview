from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = "todos"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime)
    comments = db.relationship("Comment")
    
    def __init__(self, title, deadline):
        self.title = title
        self.deadline = deadline
        
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=True)
    todo_id = db.Column(db.Integer, db.ForeignKey('todos.id'), nullable=True)
    
    def __init__(self, content):
        self.content = content