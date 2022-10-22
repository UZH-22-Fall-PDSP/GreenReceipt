import re
import requests
from bs4 import BeautifulSoup

def urlValidCheck(input:str):
    # # INPUT(string) : Recipe URL from food.com
    # # OUTPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html

    EXPECTED_RECIPE_PAGE = 'food.com/recipe/'

    input.index(EXPECTED_RECIPE_PAGE)

    input = input.split('?')[0]
    url = input + '?units=metric&scale=1'

    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, features="html.parser")

    return soup

def recipeIngredient(soup:BeautifulSoup):
    # # INPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html
    # # OUTPUT(tuple | string, List of dictionary) : Recipe Title and Ingredients List

    recipeTitle = soup.title.text.split(' - Food.com')[0]
    ingrdList = findIngredient(soup)
    return recipeTitle, ingrdList

def findIngredient(soup:BeautifulSoup):
    # # INPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html
    # # OUTPUT(List of dictionary) : Ingredient Information List
    # #                              {'ingredient' : string, 'quantity' : float, 'unit' : string}

    ingrdList = []

    ultag = soup.find('ul', {'class': re.compile('^ingredient-list')})

    for litag in ultag.find_all('li'):
        quant_obj = litag.find('span', {'class': re.compile('quantity')})
        ingrd_obj = litag.find('span', {'class': re.compile('text')})

        # CHECK : the item of list is the information of an ingredient.
        if (quant_obj != None) and (ingrd_obj != None):
            q = float(quant_obj.text)

            # ASSUME : If there is no unit, the unit as 'ea'
            _u = ingrd_obj.text.split()[0]
            u = _u if (_u =='ml' or _u =='g') else 'ea'

            # CHECK : the ingredient has a url for a detail.
            ingrdPage = ingrd_obj.find('a')
            if (ingrdPage != None):
                sub_url = ingrdPage['href']
                # CHECK : the ingrdient url is a Ingredient Detail page
                if ('about' in sub_url):
                    sub_url ='https://www.food.com' + sub_url
                    sub_r = requests.get(sub_url)
                    sub_html_doc = sub_r.text
                    sub_soup = BeautifulSoup(sub_html_doc, features="html.parser")
                    ingrd = sub_soup.find('h1').text
                    
                    ingrdList.append({'ingredient' : ingrd, 'quantity' : q, 'unit' : u})
                else:
                    True
                    # TODO Recursive Call of Scraping Recipe Page. Skip now.
            else:
                True
        else:
            True

    return ingrdList