import psycopg2
import sqlalchemy as db
from sqlalchemy.sql import text


"""
[CREATE]
NLP_Result (ingrd, searchedingred1, similarity1, searchedingred2, similarity2, searchedingred3, similarity3)
USER_History (recipe name, co2 totla, list of co2 by ingred)

[INSERT]
synonyms_en (ingrd, searchedingred1)
"""

CO2_REF_DB = 'postgresql://readonly:!JjFlGMjREf53965EvE@35.228.50.60:5432/postgres'
CO2_GCP_DB = None

class greenrecipe_db():

    def __init__(self):

        self.ref_db_engine = db.create_engine(CO2_REF_DB)
        self.ref_db_con = self.ref_db_engine.connect()

        # self.gcp_db_engine = db.create_engine(CO2_GCP_DB)
        # self.gcp_db_con = self.gcp_db_engine.connect()

    def search_ingrdCO2_total(self, ingrdList):
        # # INPUT(List of dictionary) : Ingredient Information List
        # #                              {'ingredient' : string, 'quantity' : float, 'unit' : string}
        # # OUTPUT(Tuple) : Total CO2, 
        #                   Ingredient CO2 Information List
        #                   { "ingredient" : <str: Ingredient name>, "co2" : <float: CO2 emission> }

        ingrdList_co2 = []
        total_co2 = 0
        for ingrd in ingrdList:

            ingrd_name = ingrd['ingredient']

            s = text(
                "SELECT DISTINCT(emissions) "
                "FROM emissions "
                "WHERE ingredient = :val "
            )

            # TODO [CORNER CASE] handle the case that many items with the same ingredient name e.g. 'corn'
            # For now, just return the top value
            co2 = round(ingrd['quantity'] * self.ref_db_con.execute(s, val = ingrd_name).all()[0][0], 2)
            total_co2 = round(total_co2,2) + co2
            ingrdList_co2.append({'ingredient' : ingrd_name, 'co2' : co2})

        return total_co2, ingrdList_co2

    def update_user_request(ingrd):
        # Input : {"name" : <str: receipt name>, "emissions" : <int: CO2 emissions>, "url" : <str: link>}
        # output : null
        return 