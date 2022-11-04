from scipy.spatial import distance
import fasttext


class greenrecipe_nlp():
  def __init__(self, ingrd_list):

    self.ft = fasttext.load_model('../model/fastText/cc.en.300.bin')
    self.ingrd_list = ingrd_list ## Unique Ingredient List from the Emissions Table
    self.ingrd_db_wvs = [] ## Word vector list of Unique Ingredient List from the Emissions Table

    for ingrd in ingrd_list:
      self.ingrd_db_wvs.append(self.ft.get_word_vector(ingrd))

  def find_similar_ing(self, recipeIngrdList):

    ref_name_list = self.ingrd_list
    ref_vector_list = self.ingrd_db_wvs
    update_history = []

    for i, recipeIngrd in enumerate(recipeIngrdList):

      dist = []
      
      name = recipeIngrd['ingredient']
      vector = self.ft.get_word_vector(name)   

      for ref_vector in ref_vector_list:
        cos_sim = distance.cosine(vector, ref_vector)
        dist.append(cos_sim)

      dist_unsorted = dist.copy()
      dist.sort()

      rank1_value = dist[0]
      rank1 = ref_name_list[dist_unsorted.index(rank1_value)]
      rank2_value = dist[1]
      rank2 = ref_name_list[dist_unsorted.index(rank2_value)]
      rank3_value = dist[2]
      rank3 = ref_name_list[dist_unsorted.index(rank3_value)]

      if recipeIngrdList[i]['ingredient'] != rank1:

        recipeIngrdList[i]['ingredient'] = rank1

        update_history.append({'ingrd': name, 
                                'res': [(rank1, rank1_value),
                                        (rank2, rank2_value),
                                        (rank3, rank3_value)]})

      
    return  recipeIngrdList, update_history