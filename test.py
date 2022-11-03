import re
import requests
from bs4 import BeautifulSoup

import greenrecipe_web as web
import greenrecipe_db as db
import greenrecipe_nlp as nlp
import greenrecipe_total as total
from sqlalchemy.orm import Session

import json

gr = total.greenrecipe()

# input = 'https://www.food.com/recipe/creamy-cajun-chicken-pasta-39087'
input = 'creamy-cajun-chicken-pasta-39087'
# input = 'sweet-and-spicy-vegetarian-chili-97649'

result = gr.get_co2_emissions(input, True)
print('\n\n\n',result)