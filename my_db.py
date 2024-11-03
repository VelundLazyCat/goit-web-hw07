from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# URI: postgresql://username:password@domain:port/database


engine = create_engine("sqlite:///myhomework-07.db")
Session = sessionmaker(bind=engine)
session = Session()
