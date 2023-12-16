from models import Order, Dish, Customer, session

order1 = Order(dish_id=2, customer_id=1, time='17:00:00', payment_method='cash')

session.add(order1)
session.commit()
