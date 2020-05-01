from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql+pg8000://postgres:docker@localhost/testdocker', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class User(Base):
    __tablename__='users'
    id = Column(Integer, primary_key=True)
    name = Column(String(40), index=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def save(self):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise
    def delete(self):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(String(40))
    symbol = Column(String(10))
    price = Column(String(15))

    pessoa_id = Column(Integer, ForeignKey('users.id'))
    pessoa = relationship("User")

    def __repr__(self):
        return '<Company {}>'.format(self.name)

    def save(self):
        try:
            db_session.add(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

    def delete(self):
        try:
            db_session.delete(self)
            db_session.commit()
        except:
            db_session.rollback()
            raise

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()