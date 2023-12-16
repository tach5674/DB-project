from models import Order, Dish, Customer, session
import random

names = [
    "Jeffery", "Jessica", "David", "Caitlin", "Emily", "Daniel", "Amanda", "Sean", "Rachel", "Stephen",
    "Patrick", "Laura", "Karen", "Jacob", "Lisa", "Michael", "Megan", "Christopher", "Olivia", "Matthew",
    "Samantha", "Joshua", "Michelle", "Ryan", "Ashley", "Kevin", "Sarah", "Nicholas", "Kimberly", "Brian",
    "Jennifer", "Eric", "Angela", "Jonathan", "Melissa", "Justin", "Brittany", "Anthony", "Amanda", "Tyler",
    "Stephanie", "Benjamin", "Elizabeth", "Charles", "Nicole", "Jeremy", "Heather", "Timothy", "Lauren", "Gregory"
]

surnames = [
    "May", "Casey", "Webb", "Evans", "Kim", "Miller", "Lee", "Chavez", "Simpson", "Carter",
    "Scott", "Taylor", "Wilson", "Phillips", "Hall", "Martinez", "Lopez", "Wright", "Hernandez", "Johnson",
    "Brown", "Thompson", "Young", "Adams", "Rodriguez", "King", "Moore", "Lewis", "Clark", "Foster",
    "Baker", "Davis", "White", "Turner", "Allen", "Cooper", "Perez", "Cook", "Brooks", "Ramirez",
    "Long", "Hughes", "Ward", "Price", "Bailey", "Murphy", "Torres", "Reed", "Russell", "Campbell"
]

ages = list()
for _ in range(50):
    ages.append(random.randint(18, 80))

organizations = [
    "Apex Industries", "Global Solutions Inc.", "Pioneer Enterprises", "Innovate Innovations", "Vanguard Corporation",
    "Summit Innovations", "Unified Services Group", "Frontier Technologies", "Elevate Enterprises", "Vertex Holdings",
    "Strategic Partners Inc.", "Prime Ventures", "Endeavor Industries", "Elite Enterprises", "Omega Solutions",
    "Synergy Corporation", "Syntech Innovations", "NexGen Services", "Profound Ventures", "Zenith Industries",
    "Alliance Holdings", "Apex Innovations", "Pinnacle Enterprises", "Supreme Solutions", "Focus Enterprises",
    "Innova Group", "Crest Corporation", "Horizon Technologies", "Empire Innovations", "Aegis Holdings",
    "Innovative Solutions Inc.", "Excellence Enterprises", "Optimal Ventures", "Eclipse Innovations",
    "Fusion Industries",
    "Ascend Corporation", "Oasis Holdings", "Evolve Enterprises", "Quantum Solutions", "New Horizons Group",
    "Frontline Ventures", "Visionary Technologies", "Apex Systems", "Prime Solutions", "Vista Innovations",
    "Bright Ventures", "Everest Holdings", "Frontiers Inc.", "Summit Innovations", "RAU"
]

for i in range(50):
    data = {'first_name': names[i],
            'second_name': surnames[i],
            'age': ages[i],
            'organisation': organizations[i],
            'preferences': 'none'
            }
    session.add(Customer(**data))
session.commit()

dish_names = [
    "Spaghetti Carbonara", "Chicken Tikka Masala", "Pad Thai", "Sushi Rolls", "Lasagna", "Hamburger", "Pizza Margherita",
    "Beef Stroganoff", "Tacos", "Ramen", "Caesar Salad", "Steak Frites", "Fish and Chips", "Pasta Primavera",
    "Barbecue Ribs", "Butter Chicken", "Mushroom Risotto", "Chili Con Carne", "Fettuccine Alfredo", "Biryani",
    "Chicken Parmesan", "Shrimp Scampi", "Greek Salad", "Hummus and Pita", "Cobb Salad", "Beef Burrito", "Pho",
    "Tom Yum Soup", "Gyoza", "Ratatouille", "Beef Wellington", "Kung Pao Chicken", "Falafel Wrap", "Shepherd's Pie",
    "Pesto Pasta", "Sushi Sashimi", "Pad See Ew", "Buffalo Wings", "Teriyaki Salmon", "Eggplant Parmesan",
    "Beef Tacos", "Caprese Salad", "Stuffed Bell Peppers", "Chicken Noodle Soup", "Lemon Garlic Shrimp", "Pulled Pork",
    "Chicken Fried Rice", "Ceviche", "egg", "tea"
]

categories = ['breakfast', 'dinner', 'desert', 'lunch']

prices = list()
for _ in range(50):
    prices.append(random.randint(1, 30))

calories = list()
for _ in range(50):
    calories.append(random.randint(50, 500))

weight = list()
for _ in range(50):
    weight.append(random.randint(50, 1000))

for i in range(50):
    data = {'name': dish_names[i],
            'price': prices[i],
            'category': categories[i % len(categories)],
            'calories': calories[i],
            'weight': weight[i]
            }
    session.add(Dish(**data))
session.commit()
