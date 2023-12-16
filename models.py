from sqlalchemy import create_engine, Column, Integer, String, Float, Time, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="mypassword",
    host="localhost",
    database="canteen",
    port=5432
)

engine = create_engine(url)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"

    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    time = Column(Time)
    payment_method = Column(String)


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float(precision=2))
    category = Column(String)
    calories = Column(Integer)
    weight = Column(Integer)

    customers = relationship("Customer", secondary="orders", back_populates="dishes")


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    second_name = Column(String, index=True)
    age = Column(Integer)
    organisation = Column(String)
    preferences = Column(String)
    weight = Column(Integer)

    dishes = relationship("Dish", secondary="orders", back_populates="customers")


Base.metadata.create_all(bind=engine)
