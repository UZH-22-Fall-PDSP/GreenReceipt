import greenrecipe_db as db
import greenrecipe_nlp as nlp
import greenrecipe_web as web



class greenrecipe():
    
    def __init__(self):
        self.grp_db = db.greenrecipe_db()
        self.grp_nlp = nlp.greenrecipe_nlp(self.grp_db.get_ingrd_list())

    def get_co2_emissions(self, recipe, verbose = False):
        if verbose:
            print("----------------------------------------")
            print("## Web Scraping ....")

        urlsoup = web.requestRecipeUrl(recipe)
        recipeName, ingrdList = web.parseRecipeIngrd(urlsoup)

        if verbose:
            print(recipeName, ingrdList)
            print("----------------------------------------")
            print("## NLP for Ingredient ....")

        ingrdList, update_history = self.grp_nlp.find_similar_ing(ingrdList)

        if verbose:
            print(update_history)
            print("----------------------------------------")
            print("## Calculate CO2 ....")

        total_co2, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(ingrdList)

        if verbose:
            print(total_co2)
            print("----------------------------------------")

        return {'recipeName' : recipeName, 'totalCO2': total_co2, 'ingrdCO2List': ingrdList_co2}