from sqlalchemy import ForeignKey, Column, Integer, String, MetaData, Boolean, create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)


#one to many relationship
class Audition(Base):
    __tablename__ = 'auditions'
    id = Column(Integer, primary_key=True)
    actor = Column(String())
    location = Column(String())
    phone = Column(Integer())
    hired = Column(Boolean())
    role_id = Column(Integer, ForeignKey('roles.id'))

    role = relationship('Role', backref='auditions')

    def call_back(self):
        self.hired = True

# Audition.role returns an instance of role associated with this audition.
# Audition.call_back() will change the the hired attribute to True.

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    character_name = Column(String())
    
    # audition = relationship('Audition', back_populates='roles')

    def actors(self):
        return[audition.actor for audition in self.auditions]
    def locations(self):
        return[audition.location for audition in self.auditions]
    def lead(self):
        hired_auditions = [audition for audition in self.audition if audition.hired]
        return hired_auditions[0] if hired_auditions else "no actor has been hired for this role"
    def understudy(self):
        hired_auditions = [audition for audition in self.audition if audition.hired]
        return hired_auditions[1] if len(hired_auditions) > 1 else 'no actor has been hired for understudy for this role'
    
    

Theater_engine = create_engine('sqlite:///Moringa_Theater.db')
Base.metadata.create_all(Theater_engine)
Session = sessionmaker(bind=Theater_engine)
session = Session()
