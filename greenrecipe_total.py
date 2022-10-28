import greenrecipe_db as db
import greenrecipe_nlp as nlp
import greenrecipe_web as web



class greenrecipe():
    
    def __init__(self):
        self.grp_db = db.greenrecipe_db()

    def get_co2_emissions(self, recipe):

        urlsoup = web.requestRecipeUrl(recipe)
        recipeName, ingrdList = web.parseRecipeIngrd(urlsoup)

        ingrdList = nlp.find_similar_ing(ingrdList)
        
        total_co2, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(ingrdList)
        
        return {'recipeName' : recipeName, 'totalCO2': total_co2, 'ingrdCO2List': ingrdList_co2}