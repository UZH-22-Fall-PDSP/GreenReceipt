import greenrecipe_db as db
import greenrecipe_nlp as nlp
import greenrecipe_web as web

import random
import string

class greenrecipe():
    
    def __init__(self):
        print("----------------------------------------")
        self.grp_db = db.greenrecipe_db()
        print("## db constructor success!")
        print("GCP DB Tables : ",self.grp_db.gcp_db_engine.table_names())   
        print("REF DB Tables : ",self.grp_db.ref_db_engine.table_names())   
        print("----------------------------------------") 
        self.grp_nlp = nlp.greenrecipe_nlp(self.grp_db.get_ingrd_list())
        print("## nlp constructor success!")  

    def get_co2_emissions(self, recipe, verbose = False):
        if verbose: print("----------------------------------------\n## Web Scraping ....")
        urlsoup = web.requestRecipeUrl(recipe)

        recipeName = web.parseRecipeName(urlsoup)
        isExist, total_co2, ingrdList_co2 = self.grp_db.search_recipe_in_db(recipeName)

        if isExist:
            # In case the total_co2 of this recipe was calculated before.
            if verbose: print("----------------------------------------\n## Recipe already in userhistory DB ....")
        else:
            # In case the total_co2 of this recipe is new.
            if verbose: print("## Scraping recipe ingredients ....")
            ingrdList = web.parseRecipeIngrd(urlsoup)
            if verbose: print(f"{recipeName}\n{ingrdList}\n----------------------------------------\n## NLP for Ingredient ....")
            ingrdList, update_history = self.grp_nlp.find_similar_ing(ingrdList)

            """
            TODO Temporary Dataset for update_history
            # ingrd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            # update_history = [{'ingrd':ingrd,'result':[('A',0.01),('B',0.01),('C',0.01)]}]
            """

            if verbose: print(f"{update_history}\n## Update nlpsimresult DB ....")
            self.grp_db.update_nlpsimresult(update_history)

            if verbose: print("----------------------------------------\n## Calculate CO2 ....")
            total_co2, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(ingrdList)

            if verbose: print("## Update userhistory DB ....")
            self.grp_db.update_userhistory(recipeName, total_co2, ingrdList_co2)

        if verbose: print(f"{total_co2}\n----------------------------------------\nDone!")
            
        return {'recipeName' : recipeName, 'totalCO2': total_co2, 'ingrdCO2List': ingrdList_co2}