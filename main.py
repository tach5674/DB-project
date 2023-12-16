import sqlalchemy
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

app = FastAPI()

# Define SQLAlchemy models
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mypassword@localhost/canteen"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = sqlalchemy.orm.declarative_base()


class Dish(Base):
    __tablename__ = "dishes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Float(precision=2))
    category = Column(String)
    calories = Column(Integer)
    weight = Column(Integer)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)

