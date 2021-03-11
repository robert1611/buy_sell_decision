from sqlalchemy import create_engine
from sqlalchemy import Column, Float, String, Integer, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from os import environ

db_string = environ['POSTGRES_DB_URL']

db = create_engine(db_string)
base = declarative_base()

class RentRef_3(base):
    __tablename__ = 'rent_ref_3'

    id = Column(Integer, primary_key=True)
    rent = Column(Integer)
    zip_code = Column(String)

class DecisionMaker(base):
    __tablename__ = 'decision_maker'

    id = Column(Integer, primary_key=True)
    house_purchase_value = Column(Float)
    mortgage_percent = Column(Float)
    property_tax = Column(Float)
    repairs_cost = Column(Float)
    insurance_cost = Column(Float)
    mortgage_interest= Column(Float)
    house_purchase_cost_per_month = Column(Float)
    amortized_transaction_cost = Column(Float)
    house_rent_value_per_month= Column(Float)
    option_result = Column(String)
    years_to_live = Column(Integer)
    zip_code = Column(String)
    credit_score = Column(String)
    has_been_bankrupt = Column(Integer)

class User(base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True)
  email = Column(String)
  display_name = Column(String)
  google_id = Column(String)
  facebook_id = Column(String)

class Housing(base):
  __tablename__ = 'housing'

  zip_code = Column(String, primary_key=True)
  city_state = Column(String)
  median_price = Column(Float)
  median_price_sqft = Column(Float)
  median_sqft = Column(Float)
  total_listing_count = Column(Integer)

  UniqueConstraint('email', name='uix_email')

  def is_active(self):
    return True

  def get_id(self):
    return self.email

  def is_authenticated(self):
    return self.authenticated

  def is_anonymous(self):
    return False

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)




def get_rent_by_zip_code(zip_code):
  rent_record = session.query(RentRef_3.rent).filter(RentRef_3.zip_code==zip_code).first()
  print(rent_record)
  return rent_record[0]

def get_value_by_zip_code(zip_code):
  price_record = session.query(Housing.median_price).filter(Housing.zip_code==zip_code).first()
  print(price_record)
  return price_record[0]