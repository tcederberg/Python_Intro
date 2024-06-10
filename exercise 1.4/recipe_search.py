import pickle

def display_recipe(recipe):
    print('Name:', recipe['Name'])
    print('Cooking_time:', recipe['Cooking_time'])
    print('Ingredients: ', recipe['Ingredients'])
    print('Difficulty: ', recipe['Difficulty'])
    
def search_ingredient(data):
    all_ingredients = data['all_ingredients']
    all_ingredients_indexed = list(enumerate(all_ingredients, 1))
    
    for ingredient in all_ingredients_indexed:
        print('No.', ingredient[0], ' - ', ingredient[1])
        
    try:
        num = int(input("please choose the number for the ingredient you would like : ")) 
        index = num - 1
        ingredient_search = all_ingredients[index]
        ingredient_search = ingredient_search.lower()
        
    except IndexError:
        print('sorry, the number you have chosen isnt available')
        
    except:
        print('unxpected error while searching,please try again.')
        
    else:
        for recipe in data['recipes_list']:
                if ingredient_search in recipe['Ingredients']:
                    print('\nThe following recipe includes the following ingredients')
                    print('--------------------------')
                    display_recipe(recipe)


filename = input("please enter the filename with your recipes -") + ".bin"

try:
    recipes_file = open(filename, 'rb')
    data = pickle.load(recipes_file)
    
except FileNotFoundError:
    print('this file doesnt exist in this directory')   
    data = { 'recipes_list':[], 'all_ingredients':[] } 

else:
    search_ingredient(data)
finally:
    recipes_file.close()