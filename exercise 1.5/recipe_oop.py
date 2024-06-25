# Class Definition: Recipe

class Recipe:
    # Class variable to store all ingredients from all recipes
    all_ingredients = set()

    def __init__(self, name, cooking_time):
        # Initialization method with name and cooking time
        self.name = name  # Recipe name
        self.ingredients = []  # List to store recipe ingredients
        self.cooking_time = cooking_time  # Cooking time in minutes
        self.difficulty = None  # Difficulty level, to be calculated in later function

    def add_ingredients(self, *args):
        # Add ingredients to the recipe
        for ingredient in args:
            self.ingredients.append(ingredient)
        self.update_all_ingredients()  # Update the class variable with new ingredients

    def update_all_ingredients(self):
        # Update the class variable all_ingredients with ingredients
        for ingredient in self.ingredients:
            Recipe.all_ingredients.add(ingredient)

    def calculate_difficulty(self):
        # Calculate the difficulty level based on cooking time and number of ingredients
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def get_name(self):
        # Getter for the recipe name
        return self.name

    def set_name(self, name):
        # Setter for the recipe name
        self.name = name

    def get_cooking_time(self):
        # Getter for the cooking time
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        # Setter for the cooking time
        self.cooking_time = cooking_time

    def get_ingredients(self):
        # Getter for the ingredients list
        return self.ingredients

    def get_difficulty(self):
        # Getter for the difficulty with calculations if not completed already
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        # Search for an ingredient in the recipe
        return ingredient in self.ingredients

    def __str__(self):
        # String representation of the recipe
        self.calculate_difficulty()
        return f"Recipe Name: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.difficulty}"


# Function: recipe_search
def recipe_search(data, search_term):
    # Search for recipes containing a specific ingredient
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


# Main code
# Creating instances of the Recipe class and adding ingredients
tea = Recipe("Tea", 5)
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
print(tea)

coffee = Recipe("Coffee", 5)
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
print(coffee)

cake = Recipe("Cake", 50)
cake.add_ingredients(
    "Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"
)
print(cake)

banana_smoothie = Recipe("Banana Smoothie", 5)
banana_smoothie.add_ingredients(
    "Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes"
)
print(banana_smoothie)

# Creating a list of recipes
recipes_list = [tea, coffee, cake, banana_smoothie]

# Using recipe_search function to find recipes containing specific ingredients
print("\nRecipes containing Water:")
recipe_search(recipes_list, "Water")

print("\nRecipes containing Sugar:")
recipe_search(recipes_list, "Sugar")

print("\nRecipes containing Bananas:")
recipe_search(recipes_list, "Bananas")