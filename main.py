import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends, Query
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Time
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

app = FastAPI()

# Define SQLAlchemy models
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mypassword@localhost/canteen"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Order(Base):
    __tablename__ = "orders"
    dish_id = Column(Integer, ForeignKey('dishes.id'), primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), primary_key=True)
    time = Column(Time)
    payment_method = Column(String)


@app.post("/orders/")
def add_order(dish_id: int, customer_id: int, time: str, payment_method: str, db: Session = Depends(get_db)):
    new_order = Order(dish_id=dish_id, customer_id=customer_id, time=time, payment_method=payment_method)
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order added successfully"}


@app.get("/orders/{order_id}")
def get_order_by_id(dish_id: int, customer_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.customer_id == customer_id, Order.dish_id == dish_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/{order_id}")
def update_order(dish_id: int, customer_id: int, time: str, payment_method: str, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.customer_id == customer_id, Order.dish_id == dish_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order.time = time
    order.payment_method = payment_method
    db.commit()
    db.refresh(order)
    return order


@app.delete("/orders/{dish_id}/{customer_id}")
def delete_order(dish_id: int, customer_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.customer_id == customer_id, Order.dish_id == dish_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}


@app.get("/orders/")
def get_orders(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, le=100),
               db: Session = Depends(get_db)):
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float(precision=2))
    category = Column(String)
    calories = Column(Integer)
    weight = Column(Integer)

    customers = relationship("Customer", secondary="orders", back_populates="dishes")


@app.post("/dishes/")
def add_dish(name: str, price: float, category: str, calories: int, weight: int, db: Session = Depends(get_db)):
    new_dish = Dish(name=name, price=price, category=category, calories=calories, weight=weight)
    db.add(new_dish)
    db.commit()
    db.refresh(new_dish)
    return {"message": "Dish added successfully"}


@app.get("/dishes/{dish_id}")
def get_dish_by_id(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@app.put("/dishes/{dish_id}")
def update_dish(dish_id: int, name: str, price: float, category: str, calories: int, weight: int,
                db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    dish.name = name
    dish.price = price
    dish.category = category
    dish.calories = calories
    dish.weight = weight
    db.commit()
    db.refresh(dish)
    return dish


@app.delete("/dishes/{dish_id}")
def delete_dish(dish_id: int, db: Session = Depends(get_db)):
    dish = db.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    db.delete(dish)
    db.commit()
    return {"message": "Dish deleted successfully"}


@app.get("/dishes/")
def get_dishes(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, le=100),
               db: Session = Depends(get_db)):
    dishes = db.query(Dish).offset(skip).limit(limit).all()
    return dishes


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    second_name = Column(String, index=True)
    age = Column(Integer)
    organisation = Column(String)
    preferences = Column(String)

    dishes = relationship("Dish", secondary="orders", back_populates="customers")


@app.post("/customers/")
def add_customer(first_name: str, second_name: str, age: int, organisation: str, preferences: str,
                 db: Session = Depends(get_db)):
    new_customer = Customer(first_name=first_name, second_name=second_name, age=age, organisation=organisation,
                            preferences=preferences)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return {"message": "Customer added successfully"}


@app.get("/customers/{customer_id}")
def get_customer_by_id(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.put("/customers/{customer_id}")
def update_customer(customer_id: int, first_name: str, second_name: str, age: int, organisation: str, preferences: str,
                    db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.first_name = first_name
    customer.second_name = second_name
    customer.age = age
    customer.organisation = organisation
    customer.preferences = preferences
    db.commit()
    db.refresh(customer)
    return customer


@app.delete("/customers/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(customer)
    db.commit()
    return {"message": "Customer deleted successfully"}


@app.get("/customers/")
def get_customers(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, le=100),
                  db: Session = Depends(get_db)):
    customers = db.query(Customer).offset(skip).limit(limit).all()
    return customers


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
