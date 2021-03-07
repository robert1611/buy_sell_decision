from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

db_string = environ['POSTGRES_DB_URL']

db = create_engine(db_string)
base = declarative_base()

class RentRef(base):
    __tablename__ = 'rent_ref'

    id = Column(Integer, primary_key=True)
    rent = Column(Integer)
    zip_code = Column(String)
    bedroom_number = Column(Integer)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

def get_rent_by_zip_code(zip_code, no_of_bedrooms):
  rent_record = session.query(RentRef).filter(RentRef.zip_code==zip_code, RentRef.bedroom_number== no_of_bedrooms).first()
  print(rent_record)
  return rent_record.rent