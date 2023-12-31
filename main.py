from fastapi import FastAPI, HTTPException, Query
from models import Order, Dish, Customer, session
from sqlalchemy import update, select, func
import uvicorn

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
async def get_orders(page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size
    data = session.query(Order).order_by(Order.dish_id, Order.customer_id).all()
    data_length = len(data)
    response = {
        "data": data[start:end],
        "total": data_length,
        "count": page_size,
        "pagination": {}
    }
    if end > data_length:
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"/orders/get?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"/orders/get?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"/orders/get?page_num={page_num + 1}&page_size={page_size}"

    return response


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
async def get_dishes(page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size
    data = session.query(Dish).order_by(Dish.id).all()
    data_length = len(data)
    response = {
        "data": data[start:end],
        "total": data_length,
        "count": page_size,
        "pagination": {}
    }
    if end > data_length:
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"/dishes/get?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"/dishes/get?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"/dishes/get?page_num={page_num + 1}&page_size={page_size}"

    return response


@app.put("/dishes/update")
async def update_price_by_category(amount: float, category: str):
    try:
        session.execute(update(Dish).where(Dish.category == category).values(price=Dish.price + amount))
        session.commit()
        return {"message": f"Dishes from category: {category} price raised by {amount}"}
    except Exception as e:
        session.rollback()
        return {"error": str(e)}


@app.get("/dishes/select")
async def get_dishes_by_price(price_from: int = 1, price_to: int = 30):
    data = session.query(Dish).order_by(Dish.price).filter(price_from <= Dish.price, Dish.price <= price_to).all()
    response = {
        "data": data,
        "total": len(data),
    }
    return response


@app.post("/customers/add")
async def add_customer(first_name: str, second_name: str, age: int, organisation: str, preferences: str, weight: int):
    new_customer = Customer(first_name=first_name, second_name=second_name, age=age, organisation=organisation,
                            preferences=preferences, weight=weight)
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
                          preferences: str, weight: int):
    customer = session.query(Customer).filter(Customer.id == customer_id).first()
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    customer.first_name = first_name
    customer.second_name = second_name
    customer.age = age
    customer.organisation = organisation
    customer.preferences = preferences
    customer.weight = weight
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
async def get_customers(page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size
    data = session.query(Customer).order_by(Customer.id).all()
    data_length = len(data)
    response = {
        "data": data[start:end],
        "total": data_length,
        "count": page_size,
        "pagination": {}
    }
    if end > data_length:
        response["pagination"]["next"] = None

        if page_num > 1:
            response["pagination"]["previous"] = f"/customers/get?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None
    else:
        if page_num > 1:
            response["pagination"]["previous"] = f"/customers/get?page_num={page_num - 1}&page_size={page_size}"
        else:
            response["pagination"]["previous"] = None

        response["pagination"]["next"] = f"/customers/get?page_num={page_num + 1}&page_size={page_size}"

    return response


@app.get("/customers/orders")
async def join_customers_orders():
    results = (session.query(Order.dish_id, Customer.first_name, Dish.name)
               .join(Dish, Order.dish_id == Dish.id)
               .join(Customer, Order.customer_id == Customer.id).all())
    for row in results:
        print(f"Order ID: {row[0]}, Customer Name: {row[1]}, Dish Name: {row[2]}")
    return


@app.get("/dishes")
async def group_by_category():
    results = session.query(Dish.category, func.count(Dish.id)).group_by(Dish.category).all()
    for row in results:
        print(f'There are {row[1]} dishes in {row[0]} category.')
    return


if __name__ == "__main__":
    uvicorn.run(app, port=8000)
