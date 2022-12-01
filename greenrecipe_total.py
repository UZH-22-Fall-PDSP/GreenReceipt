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
        print("----------------------------------------") 
        self.grp_nlp = nlp.greenrecipe_nlp(self.grp_db.get_ingrd_list())
        print("## nlp constructor success!")  

    def get_recipe_co2_emissions(self, recipe, verbose = False):

        if verbose: print("----------------------------------------\n## 1. SCARPING URL ....")
        urlsoup = web.requestRecipeUrl(recipe, verbose)
        recipeName = web.parseRecipeName(urlsoup, verbose)

        if verbose: print("----------------------------------------\n## 2. CHECKING userHistory DB ....")
        isExist, total_co2, ingrdList_co2 = self.grp_db.search_recipe_in_db(recipeName, verbose)

        if not(isExist):
            # In case the total_co2 of this recipe is new.
            if verbose: print("----------------------------------------\n## 3. PREPARING Ingredients Data")
            ingrdList = web.parseRecipeIngrd(urlsoup, verbose)
            ingrdList, update_history, _ = self.grp_nlp.find_similar_ing(ingrdList, verbose)
            self.grp_db.update_nlpsimresult(update_history, verbose)

            if verbose: print("----------------------------------------\n## 4. CALCULATING Recipe CO2 Total....")
            total_co2, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(ingrdList, verbose)
            self.grp_db.update_userhistory(recipeName, total_co2, ingrdList_co2, verbose)

        if verbose: print(f"----------------------------------------\n## 5. RESULT {recipeName}...\n{total_co2}\n{ingrdList_co2}\n\n")
        return {'recipeName' : recipeName, 'totalCO2': total_co2, 'ingrdCO2List': ingrdList_co2}

    def get_ingrd_co2_emissions(self, ingrdList, verbose=False):

        if verbose: print("----------------------------------------\n## 1. TYPECAST Ingredient List....")
        typecast_ingrdList = []
        print(ingrdList)
        for i, ingrd in enumerate(ingrdList['ingrd']):
            _ = {}
            _['ingredient'] = ingrd
            _['quantity'] = ingrdList['ingrd_q'][i]
            _['unit'] = ingrdList['ingrd_u'][i]
            typecast_ingrdList.append(_)
        typecast_ingrdList, update_history, _ = self.grp_nlp.find_similar_ing(typecast_ingrdList, verbose)
        self.grp_db.update_nlpsimresult(update_history, verbose)

        if verbose: print("----------------------------------------\n## 2. CALCULATING Ingredients CO2....")
        total_co2, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(typecast_ingrdList, verbose)

        if verbose: print(f"----------------------------------------\n## 3. RESULT...\n{total_co2}\n{ingrdList_co2}\n\n")
        return {'totalCO2': total_co2, 'ingrdCO2List': ingrdList_co2}

    def get_simingrdset_co2_emissions(self, ingrd, verbose=False):

        ingrdList = [{'ingredient':ingrd}]
        
        if verbose: print("----------------------------------------\n## 1. PREPARING Ingredients Data")
        _, update_history, ingrdSimList = self.grp_nlp.find_similar_ing(ingrdList, verbose)
        self.grp_db.update_nlpsimresult(update_history, verbose)

        typecast_ingrdList = []
        for ingrd in ingrdSimList:
            _ = {}
            _['ingredient'] = ingrd
            _['quantity'] = 1
            _['unit'] = 'kg'
            typecast_ingrdList.append(_)
            
        if verbose: print("----------------------------------------\n## 2. CALCULATING Ingredients CO2....")
        _, ingrdList_co2 = self.grp_db.search_ingrdCO2_total(typecast_ingrdList, verbose)

        return ingrdList_co2

    def get_catingrdset_co2_emissions(self, category, verbose = False):

        if verbose: print(f"----------------------------------------\n## 1. Query Ingredients in the category")
        cat_ingrd_co2_list = self.grp_db.get_cat_ingrd_list(category, verbose)
        return cat_ingrd_co2_list


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
