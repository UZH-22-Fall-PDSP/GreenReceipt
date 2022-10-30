import greenrecipe_db as db
import greenrecipe_nlp as nlp
import greenrecipe_web as web



class greenrecipe():
    
    def __init__(self):
        print("----------------------------------------")
        self.grp_db = db.greenrecipe_db()
        print("## db constructor success!")       
        print("----------------------------------------") 
        self.grp_nlp = nlp.greenrecipe_nlp(self.grp_db.get_ingrd_list())
        print("## nlp constructor success!")  

    def get_co2_emissions(self, recipe, verbose = False):
        if verbose: print("----------------------------------------\n## Web Scraping ....")
        urlsoup = web.requestRecipeUrl(recipe)
        recipeName, ingrdList = web.parseRecipeIngrd(urlsoup)

        # isExist, total_co2, ingrdList_co2 = self.grp_db.search_recipe_in_db(recipeName)
        isExist = False
        if isExist:
            # In case the total_co2 of this recipe was calculated before.
            if verbose: print("----------------------------------------\n## Recipe in userhistory DB ....")
        else:
            # In case the total_co2 of this recipe is new.
            if verbose: print(f"{recipeName}\n{ingrdList}\n----------------------------------------\n## NLP for Ingredient ....")
            ingrdList, update_history = self.grp_nlp.find_similar_ing(ingrdList)

            if verbose: print(f"{update_history}\n## Update nlpsimresult DB ....")
            # self.grp_db.update_nlpsimresult(update_history)

            if verbose: print("----------------------------------------\n## Calculate CO2 ....")
            total_co2, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(ingrdList)

            if verbose: print("## Update userhistory DB ....")
            # self.grp_db.update_userhistory(recipeName, total_co2, ingrdList_co2)

        if verbose: print(f"{total_co2}\n----------------------------------------\nDone!")
            
        return {'recipeName' : recipeName, 'totalCO2': total_co2, 'ingrdCO2List': ingrdList_co2}