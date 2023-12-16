from fastapi import FastAPI, HTTPException, Query
from models import Order, Dish, Customer, session

app = FastAPI()


@app.post("/orders/add")
async def add_order(dish_id: int, customer_id: int, time: str, payment_method: str):
    order = Order(dish_id=dish_id, customer_id=customer_id, time=time, payment_method=payment_method)
    session.add(order)
    session.commit()
    return {"message": "Order added successfully"}


@app.get("/orders/get/{dish_id}/{customer_id}")
async def get_order_by_id(dish_id: int, customer_id: int):
    order = session.query(Order).filter(Order.customer_id == customer_id, Order.dish_id == dish_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@app.put("/orders/update/{dish_id}/{customer_id}")
async def update_order(dish_id: int, customer_id: int, time: str, payment_method: str):
    order = session.query(Order).filter(Order.customer_id == customer_id, Order.dish_id == dish_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    order.time = time
    order.payment_method = payment_method
    session.commit()
    return order


@app.delete("/orders/delete/{dish_id}/{customer_id}")
async def delete_order(dish_id: int, customer_id: int):
    order = session.query(Order).filter(Order.customer_id == customer_id, Order.dish_id == dish_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    session.delete(order)
    session.commit()
    return {"message": "Order deleted successfully"}


@app.get("/orders/get")
async def get_orders(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, le=100)):
    orders = session.query(Order).offset(skip).limit(limit).all()
    return orders


@app.post("/dishes/add")
async def add_dish(name: str, price: float, category: str, calories: int, weight: int):
    dish = Dish(name=name, price=price, category=category, calories=calories, weight=weight)
    session.add(dish)
    session.commit()
    return {"message": "Dish added successfully"}


@app.get("/dishes/get/{dish_id}")
async def get_dish_by_id(dish_id: int):
    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    return dish


@app.put("/dishes/update/{dish_id}")
async def update_dish(dish_id: int, name: str, price: float, category: str, calories: int, weight: int):
    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    dish.name = name
    dish.price = price
    dish.category = category
    dish.calories = calories
    dish.weight = weight
    session.commit()
    return dish


@app.delete("/dishes/delete/{dish_id}")
async def delete_dish(dish_id: int):
    dish = session.query(Dish).filter(Dish.id == dish_id).first()
    if dish is None:
        raise HTTPException(status_code=404, detail="Dish not found")
    session.delete(dish)
    session.commit()
    return {"message": "Dish deleted successfully"}


@app.get("/dishes/get")
async def get_dishes(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, le=100)):
    dishes = session.query(Dish).offset(skip).limit(limit).all()
    return dishes


@app.post("/customers/add")
async def add_customer(first_name: str, second_name: str, age: int, organisation: str, preferences: str):
    new_customer = Customer(first_name=first_name, second_name=second_name, age=age, organisation=organisation,
                            preferences=preferences)
    session.add(new_customer)
    session.commit()
    return {"message": "Customer added successfully"}


@app.get("/customers/get{customer_id}")
async def get_customer_by_id(customer_id: int):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.put("/customers/update/{customer_id}")
async def update_customer(customer_id: int, first_name: str, second_name: str, age: int, organisation: str,
                          preferences: str):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.first_name = first_name
    customer.second_name = second_name
    customer.age = age
    customer.organisation = organisation
    customer.preferences = preferences
    session.commit()
    return customer


@app.delete("/customers/delete/{customer_id}")
async def delete_customer(customer_id: int):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"message": "Customer deleted successfully"}


@app.get("/customers/get")
async def get_customers(skip: int = Query(default=0, ge=0), limit: int = Query(default=10, le=100)):
    customers = session.query(Customer).offset(skip).limit(limit).all()
    return customers
