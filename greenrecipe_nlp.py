import greenrecipe_web as web

import sqlalchemy as db
from scipy.spatial import distance

import fasttext


class greenrecipe_nlp():
  def __init__(self, ingrd_list):

    self.ft = fasttext.load_model('../model/fastText/cc.en.300.bin')
    self.ingrd_list = ingrd_list
    self.ingrd_db_wvs = []
    self.update_history = []

    for ingrd in ingrd_list:
      self.ingrd_db_wvs.append(self.ft.get_word_vector(ingrd))

  def find_similar_ing(self, ingredList):

    for ing_org in ingredList:
      distances = []
      ing_org_vec = self.ft.get_word_vector(ing_org['ingredient'])   

      for ing_db_vec in self.ingrd_db_wvs:
        cos_sim = distance.cosine(ing_org_vec, ing_dd_vec)
        distances.append(cos_sim)

      distances.sort()
      ingredList[i]['ingredient']= self.ingrd_list[distances.index(distances[0])]
      self.update_history.append({'ingrd': ing_org['ingredient'], 
                                  'res': [(self.ingrd_list[distances.index(distances[0])],distances[0]),
                                          (self.ingrd_list[distances.index(distances[1])],distances[1]),
                                          (self.ingrd_list[distances.index(distances[2])],distances[2])]})

      top3 = self.update_history
      
    return  ingredList, top3
    



# #################################################################################
# #This part will be run in local and saved to our GCP DB in advance
# #################################################################################
# # get all ingredient from emission table  ==> save in db and remove this block
# engine = db.create_engine('postgresql://readonly:!JjFlGMjREf53965EvE@35.228.50.60:5432/postgres')
# con = engine.connect()

# rs = con.execute('SELECT distinct(ingredient) FROM emissions')

# ing_db = []
# for r in rs:
#   ing_db.append(r[0])

# # convert all ingredient from db to vector (insert in db later)
# ft = fasttext.load_model('./model/cc.en.300.bin')


# ing_db_wv = []

# for ing in ing_db:
# 	ing_db_wv.append(ft.get_word_vector(ing))
# #################################################################################

  # def find_similar_ing(ingredList):
  #   for i, ing in enumerate(ingredList):
  #     ing_vec = ft.get_word_vector(ing['ingredient'])
  #     res = []

  #     for j, ing in enumerate(ing_db_wv):
  #       cos_sim = 1-distance.cosine(ing_vec, ing)
  #       res.append(cos_sim)

  #     ingredList[i]['ingredient']= ing_db[res.index(max(res))]
      
  #   return  ingredList




# def find_similar_ing(ingrdList):
#     # Input : <str: Ingredient Name>
#     # Output : List [<str: Ingredient Name>, <str: Ingredient Matched>]
#     ingrdList = [{'ingredient': 'peas', 'quantity': 1.0, 'unit': 'ea'}
#             , {'ingredient': 'runner beans', 'quantity': 56.69, 'unit': 'g'}
#             , {'ingredient': 'beef cold cuts', 'quantity': 14.79, 'unit': 'ml'}
#             , {'ingredient': 'apple juice', 'quantity': 1.0, 'unit': 'ea'}
#             , {'ingredient': 'peach', 'quantity': 59.14, 'unit': 'ml'}
#             , {'ingredient': 'poppy seed', 'quantity': 14.79, 'unit': 'ml'}
#             , {'ingredient': 'fish oil', 'quantity': 0.61, 'unit': 'ml'}
#             , {'ingredient': 'celery', 'quantity': 0.61, 'unit': 'ml'}
#             , {'ingredient': 'gem squash', 'quantity': 0.3, 'unit': 'ml'}
#             , {'ingredient': 'sour cream', 'quantity': 0.3, 'unit': 'ml'}
#             , {'ingredient': 'coconut', 'quantity': 29.57, 'unit': 'ml'}]
#     return ingrdList