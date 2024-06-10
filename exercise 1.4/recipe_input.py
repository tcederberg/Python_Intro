import pickle

def take_recipe():
    name = input("name of the recipe:")
    cooking_time = int(input("cooking time(min):"))
    ingredients = input("ingredients for the recipe: ").split("," or ", ")

    recipe = {
        'Name': name,
        'Cooking_time': cooking_time,
        'Ingredients': ingredients,
    }

    recipe['Difficulty'] = calc_difficulty(recipe)
    return recipe

def calc_difficulty(recipe):
    if recipe['Cooking_time'] < 10 and len(recipe['Ingredients']) <= 4:
        Difficulty = 'Easy'
    elif recipe['Cooking_time'] < 10 and len(recipe['Ingredients']) >= 4:
        Difficulty = 'Medium'
    elif recipe['Cooking_time'] >= 10 and len(recipe['Ingredients']) < 4:
        Difficulty = 'Intermediate'
    elif recipe['Cooking_time'] >= 10 and len(recipe['Ingredients']) >= 4:
        Difficulty = 'Hard'
    return Difficulty

all_ingredients = []
recipes_list = []

filename = input("please enter a filename with your recipes -") + ".bin"
data = { 'recipes_list':[], 'all_ingredients':[] }

try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)

except FileNotFoundError:
    print('file not found. creating new file')

except:
    print('unexpected error. creating new file')

else:
    recipes_file.close()

finally:
    recipes_list = data['recipes_list']
    all_ingredients = data['all_ingredients']

    num = int(input("how many recipes would you like to create? -"))

    for i in range(num):
        recipe = take_recipe()
        for ingredient in recipe['Ingredients']:
            if not ingredient in all_ingredients:
                all_ingredients.append(ingredient)
        recipes_list.append(recipe)

data = {
    'recipes_list': recipes_list,
    'all_ingredients': all_ingredients
}

recipes_file = open(filename, 'wb')
pickle.dump(data, recipes_file)
print('your file has been updated.')