import mysql.connector

# Establish a connection to the MySQL database with specified credentials
conn = mysql.connector.connect(
    host="localhost", user="cf-python", password="password", database="task_database"
)

# Create a cursor from the connection, which will be used for executing SQL commands
cursor = conn.cursor()

# SQL command to create a new table named 'Recipes' in the database if it doesn't exist already
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,  # Unique identifier for each recipe, automatically incremented
    name VARCHAR(50),                   # Name of the recipe, up to 50 characters
    ingredients VARCHAR(255),           # List of ingredients, up to 255 characters
    cooking_time INT,                   # Time required for cooking, in minutes
    difficulty VARCHAR(20)              # Difficulty level of the recipe
)
"""
)


# Function definition for the main menu of the application
def main_menu():
    while True:
        # Prompting the user to choose an option from the main menu
        choice = input(
            "Choose an option: [1] Add Recipe [2] Search Recipe [3] Update Recipe [4] Delete Recipe [5] Exit\n"
        )

        # Execute corresponding functions based on the user's choice
        if choice == "1":
            create_recipe(cursor)  # Function to add a new recipe
        elif choice == "2":
            search_recipe(cursor)  # Function to search for recipes by ingredient
        elif choice == "3":
            update_recipe(cursor)  # Function to update an existing recipe
        elif choice == "4":
            delete_recipe(cursor)  # Function to delete a recipe
        elif choice == "5":
            break  # Exit the loop and close the program
        else:
            print("Invalid choice. Please try again.")

    # Commit any changes made to the database and close the connection when exiting the menu
    conn.commit()
    conn.close()


# Function to add a new recipe to the database
def create_recipe(cursor):
    # Collecting recipe details from the user
    name = input("Enter the name of the recipe: ")
    cooking_time = int(input("Enter cooking time (in minutes): "))
    ingredients = input("Enter ingredients (separated by a comma): ").split(",")

    # Calculating the difficulty level of the recipe
    difficulty = calculate_difficulty(cooking_time, ingredients)

    # Converting the list of ingredients into a single string
    ingredients_str = ", ".join(ingredients).strip()

    # Preparing the SQL query to insert the new recipe into the database
    query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    data = (name, ingredients_str, cooking_time, difficulty)

    # Executing the query with the provided data
    cursor.execute(query, data)


# Function to determine the difficulty level of a recipe
def calculate_difficulty(cooking_time, ingredients):
    # Assigning difficulty based on cooking time and number of ingredients
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"


# Function to search for recipes based on an ingredient
def search_recipe(cursor):
    # Retrieving all unique ingredients from the Recipes table
    cursor.execute("SELECT DISTINCT ingredients FROM Recipes")
    all_ingredients = set()

    # Populating a set with all available ingredients
    for (ingredients,) in cursor:
        all_ingredients.update(ingredients.split(", "))

    # Displaying all ingredients for user selection
    print("Available ingredients: ")
    for ingredient in all_ingredients:
        print(ingredient)

    # Asking the user to input an ingredient to search for
    search_ingredient = input("Enter an ingredient to search for recipes: ")
    query = "SELECT name, ingredients FROM Recipes WHERE ingredients LIKE %s"
    search_pattern = f"%{search_ingredient}%"

    # Executing the query and displaying matching recipes
    cursor.execute(query, (search_pattern,))
    for name, ingredients in cursor:
        print(f"Recipe: {name}, Ingredients: {ingredients}")


# Function to update an existing recipe in the database
def update_recipe(cursor):
    # Displaying all existing recipes to the user
    cursor.execute("SELECT id, name FROM Recipes")
    for id, name in cursor:
        print(f"{id}: {name}")

    # Asking the user to select a recipe to update
    recipe_id = int(input("Enter the ID of the recipe to update: "))
    column = input("Which column to update (name, cooking_time, ingredients): ")
    new_value = input(f"Enter new value for {column}: ")

    # Handling updates for 'cooking_time' and 'ingredients' columns
    if column in ["cooking_time", "ingredients"]:
        if column == "cooking_time":
            new_value = int(new_value)
        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))
        ingredients = cursor.fetchone()[0]

        # Recalculating difficulty if necessary
        difficulty = (
            calculate_difficulty(new_value, ingredients.split(", "))
            if column == "cooking_time"
            else calculate_difficulty(
                int(input("Enter cooking time: ")), new_value.split(", ")
            )
        )

        # Updating the recipe in the database
        cursor.execute(
            f"UPDATE Recipes SET {column} = %s, difficulty = %s WHERE id = %s",
            (new_value, difficulty, recipe_id),
        )
    else:
        # Updating the recipe for other columns
        cursor.execute(
            f"UPDATE Recipes SET {column} = %s WHERE id = %s", (new_value, recipe_id)
        )


# Function to delete a recipe from the database
def delete_recipe(cursor):
    # Displaying all recipes to the user for selection
    cursor.execute("SELECT id, name FROM Recipes")
    for id, name in cursor:
        print(f"{id}: {name}")

    # Asking the user to choose a recipe to delete
    recipe_id = int(input("Enter the ID of the recipe to delete: "))

    # Executing the delete operation on the selected recipe
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))


# Entry point for the script
if __name__ == "__main__":
    main_menu()