# Importing necessary modules from SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Set up SQLAlchemy Engine and Session
engine = create_engine(
    "mysql+mysqlconnector://cf-python:password@localhost:3306/task_database", echo=True
)

Session = sessionmaker(bind=engine)
session = Session()

# Creating the base class using declarative base for ORM
Base = declarative_base()


# Definition of the Recipe class
class Recipe(Base):
    __tablename__ = "final_recipes"

    # Defining columns in the table
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # Representation methods for printing the recipe information
    def __repr__(self):
        return f"<Recipe(id={self.id}, name='{self.name}', difficulty='{self.difficulty}')>"

    def __str__(self):
        return (
            f"Recipe ID: {self.id}\n"
            f"Name: {self.name}\n"
            f"Ingredients: {self.ingredients}\n"
            f"Cooking Time: {self.cooking_time} minutes\n"
            f"Difficulty: {self.difficulty}\n"
            "-----------------------------\n"
        )

    # Method to calculate difficulty based on cooking time and number of ingredients
    def calculate_difficulty(self):
        num_ingredients = len(self.ingredients.split(","))
        # Logic for determining difficulty
        if self.cooking_time < 10 and num_ingredients < 4:
            return "Easy"
        elif self.cooking_time < 10 and num_ingredients >= 4:
            return "Medium"
        elif self.cooking_time >= 10 and num_ingredients < 4:
            return "Intermediate"
        else:
            return "Hard"


# Creating tables in the database based on the above class definition
print("Creating tables...")
Base.metadata.create_all(engine)
print("Tables created successfully.")


# Function to create a new recipe
def create_recipe():
    name = input("Enter the name of the recipe (max 50 chars): ")
    ingredients_input = input("Enter the ingredients separated by a comma: ")
    cooking_time = input("Enter the cooking time in minutes: ")

    # Validate input
    if len(name) > 50 or not name.isalnum():
        print(
            "Invalid recipe name. Please ensure it is alphanumeric and less than 50 characters."
        )
        return
    if not cooking_time.isnumeric():
        print("Invalid cooking time. Please ensure it is a number.")
        return

    recipe_entry = Recipe(
        name=name, ingredients=ingredients_input, cooking_time=int(cooking_time)
    )
    recipe_entry.difficulty = recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()
    print("Recipe created successfully.")


# Function to view all recipes in the database
def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("There are no recipes in the database.")
        return

    for recipe in recipes:
        print(recipe)


# Function to search recipes by ingredients
def search_by_ingredients():
    results = session.query(Recipe.ingredients).distinct().all()
    all_ingredients = set()
    for (ingredients_str,) in results:
        all_ingredients.update(ingredients_str.split(", "))

    if not all_ingredients:
        print("There are no ingredients in the database.")
        return

    # Display ingredients
    for idx, ingredient in enumerate(all_ingredients, 1):
        print(f"{idx}. {ingredient}")

    ingredient_numbers = input(
        "Enter the numbers of the ingredients you want to search for, separated by spaces: "
    )
    ingredient_indices = ingredient_numbers.split()
    search_ingredients = [
        list(all_ingredients)[int(idx) - 1]
        for idx in ingredient_indices
        if idx.isdigit()
    ]

    conditions = [
        Recipe.ingredients.like(f"%{ingredient}%") for ingredient in search_ingredients
    ]
    recipes = session.query(Recipe).filter(*conditions).all()

    for recipe in recipes:
        print(recipe)


# Function to edit an existing recipe
def edit_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in recipes:
        print(f"{recipe_id}. {recipe_name}")

    recipe_id_to_edit = input("Enter the ID of the recipe you want to edit: ")
    if not recipe_id_to_edit.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    recipe_to_edit = session.query(Recipe).get(int(recipe_id_to_edit))
    if not recipe_to_edit:
        print("Recipe not found.")
        return

    print("1. Name\n2. Ingredients\n3. Cooking Time")
    attribute_to_edit = input("Enter the number of the attribute you want to edit: ")

    if attribute_to_edit == "1":
        new_name = input("Enter the new name: ")
        recipe_to_edit.name = new_name
    elif attribute_to_edit == "2":
        new_ingredients = input("Enter the new ingredients, separated by a comma: ")
        recipe_to_edit.ingredients = new_ingredients
    elif attribute_to_edit == "3":
        new_cooking_time = input("Enter the new cooking time in minutes: ")
        if not new_cooking_time.isnumeric():
            print("Invalid cooking time. Please enter a number.")
            return
        recipe_to_edit.cooking_time = int(new_cooking_time)

    recipe_to_edit.difficulty = recipe_to_edit.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully.")


# Function to delete a recipe
def delete_recipe():
    recipes = session.query(Recipe.id, Recipe.name).all()
    for recipe_id, recipe_name in recipes:
        print(f"{recipe_id}. {recipe_name}")

    recipe_id_to_delete = input("Enter the ID of the recipe you want to delete: ")
    if not recipe_id_to_delete.isdigit():
        print("Invalid ID. Please enter a number.")
        return

    recipe_to_delete = session.query(Recipe).get(int(recipe_id_to_delete))
    if not recipe_to_delete:
        print("Recipe not found.")
        return

    confirmation = input("Are you sure you want to delete this recipe? (yes/no): ")
    if confirmation.lower() == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print("Recipe deleted successfully.")


# Main loop for the application
# This loop presents a menu to the user and calls the appropriate function based on the user's choice
while True:
    # Displaying options and handling user input
    print("1. Create a new recipe")
    print("2. View all recipes")
    print("3. Search for recipes by ingredients")
    print("4. Edit a recipe")
    print("5. Delete a recipe")
    print("Type 'quit' to quit the application")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_recipe()
    elif choice == "2":
        view_all_recipes()
    elif choice == "3":
        search_by_ingredients()
    elif choice == "4":
        edit_recipe()
    elif choice == "5":
        delete_recipe()
    elif choice.lower() == "quit":
        break
    else:
        print("Invalid input. Please try again.")

# Closing the session and engine when the application is terminated
session.close()
engine.dispose()