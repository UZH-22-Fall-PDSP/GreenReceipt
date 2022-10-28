import re
import requests
from bs4 import BeautifulSoup

def requestRecipeUrl(input:str):
    # # INPUT(string) : Recipe name from food.com
    # # OUTPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html

    # EXPECTED_RECIPE_PAGE = 'food.com/recipe/'
    # input.index(EXPECTED_RECIPE_PAGE)
    # input = input.split('?')[0]
    
    """
    SWEET AND SPICY VEGETARIAN CHILI
    If scale is 0, there exist 0 quantity ingredients
    Solution : search with scale 10 and divide each quantity by 10 later
    """
    url = 'https://www.food.com/recipe/' + input + '?units=metric&scale=10'
    

    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, features="html.parser")

    return soup

def parseRecipeIngrd(soup:BeautifulSoup):
    # # INPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html
    # # OUTPUT(tuple | string, List of dictionary) : Recipe Title and Ingredients List

    recipeTitle = soup.title.text.split(' - Food.com')[0]
    ingrdList = findIngrd(soup)
    return recipeTitle, ingrdList

def findIngrd(soup:BeautifulSoup):
    # # INPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html
    # # OUTPUT(List of dictionary) : Ingredient Information List
    # #                              {'ingredient' : string, 'quantity' : float, 'unit' : string}

    ingrdList = []

    ultag = soup.find('ul', {'class': re.compile('^ingredient-list')})
    i = 0
    for litag in ultag.find_all('li'):
        # print(f"{i+1}/{len(ultag.find_all('li'))}")
        quant_obj = litag.find('span', {'class': re.compile('quantity')})
        ingrd_obj = litag.find('span', {'class': re.compile('text')})

        # CHECK : the item of list is the information of an ingredient.
        if (quant_obj != None) and (ingrd_obj != None):
            q_str = quant_obj.text
            q = float(q_str)/10 if q_str != '' else float(0) # scale down from 10 to 1

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

                    ingrdList.append({'ingredient' : ingrd.lower(), 'quantity' : q, 'unit' : u})
                else:
                    True
                    # TODO [CORNER CASE] Recursive Call of Scraping Recipe Page. Skip now.
            else:
                # TODO [CORNER CASE] case for the ingredient doesn't have a url link
                True
        else:
            True
        i+=1

    return ingrdList