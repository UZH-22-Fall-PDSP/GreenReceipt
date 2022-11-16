import re
import requests
from bs4 import BeautifulSoup

"""
TODO User default link without any parameter -> Get the serve value 'x' (class: adjust svelte-1o10zxc) -> User default link + ?units=metric&scale=x
            (Simple but time consuming for double scrapping)
TODO Coner case for scale 1/4
TODO Scrap non-url ingredient by using textblob
"""

def setDefaultURL(URLrecipename):
    url = 'https://www.food.com/recipe/' + URLrecipename
    r = requests.get(url)
    # get a correct url and scale to create full url
    html_doc = r.text
    soup = BeautifulSoup(html_doc, features="html.parser")
    serves = soup.find(class_="value svelte-1o10zxc").string
    # print(serves)
    if len(serves) > 0 :
      if "/" in serves:
        serves = serves.split("/")
        serves = serves[0]+"%"+"2F"+serves[1]
        # 1%2F10
    print(f"{URLrecipename}\nDefault Serve: {serves}")
    final_url = r.url + '?units=metric&scale='+serves
    return final_url

def requestRecipeUrl(input:str, verbose = False):
    # # INPUT(string) : Recipe name from food.com
    # # OUTPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html

    # EXPECTED_RECIPE_PAGE = 'food.com/recipe/'
    # input.index(EXPECTED_RECIPE_PAGE)
    # input = input.split('?')[0]
    
    # TODO: Tasks pending completion -@hyeongkyunkim at 11/15/2022, 12:55:05 PM
    # apply default serve portion to the scaping url link

    # url = 'https://www.food.com/recipe/' + input + '?units=metric&scale=10'
    url = setDefaultURL(input)
    r = requests.get(url)
    html_doc = r.text
    soup = BeautifulSoup(html_doc, features="html.parser")

    if verbose: print(f"Done - Scraping URL... {url}")

    return soup

def parseRecipeName(soup:BeautifulSoup, verbose = False):
    # # INPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html
    # # OUTPUT(tuple | string, List of dictionary) : Recipe Name
    recipeTitle = soup.title.text.split(' - Food.com')[0]

    if verbose: print(f"Done - Parsing recipe name... {recipeTitle}")

    return recipeTitle

def parseRecipeIngrd(soup:BeautifulSoup, verbose = False):
    # # INPUT(Constructor | BeautifulSoup) : BeautifulSoup constructor of Recipe URL html
    # # OUTPUT(List of dictionary) : Ingredients List
    ingrdList = findIngrd(soup)

    if verbose: print(f"DONE - Parsing recipe ingredients... {ingrdList}")

    return ingrdList

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
            q_str = quant_obj.text.split('-')
            q_str = q_str[0] # [CornerCase] e.g. 10-13
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