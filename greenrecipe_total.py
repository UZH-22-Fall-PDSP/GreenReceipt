import greenrecipe_db as db
import greenrecipe_nlp as nlp
import greenrecipe_web as web



class greenrecipe():
    
    def __init__(self):
        self.grp_db = db.greenrecipe_db()

    def get_co2_emissions(self, recipe):

        urlsoup = web.urlValidCheck(recipe)
        recipeName, ingrdList = web.recipeIngrd(urlsoup)

        ingrdList = nlp.ingrd_matching(ingrdList)
        
        total_co2, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(ingrdList)
        
        return {'recipeName' : recipeName, 'totalCO2': total_co2, 'ingrdCO2List': ingrdList_co2}