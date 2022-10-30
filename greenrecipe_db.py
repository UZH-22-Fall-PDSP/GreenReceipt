import psycopg2
import sqlalchemy
from sqlalchemy import select

from sqlalchemy.sql import text
import pandas as pd



"""
[INSERT]
synonyms_en (ingrd, searchedingred1)
"""

CO2_REF_DB = 'postgresql://readonly:!JjFlGMjREf53965EvE@35.228.50.60:5432/postgres'
CO2_GCP_DB = None

class greenrecipe_db():

    def __init__(self):

        self.ref_db_engine = sqlalchemy.create_engine(CO2_REF_DB)
        self.ref_db_con = self.ref_db_engine.connect()
        self.ref_db_emissions_df = pd.read_sql_table(
            "emissions",
            con=self.ref_db_engine,
            columns=['ingredient',
                    'emissions'],
        )

        self.gcp_db_engine = self.ref_db_engine
        self.gcp_db_con = self.ref_db_engine.connect()

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

            # TODO [CORNER CASE] handle the case that many items with the same ingredient name e.g. 'corn'
            # For now, just return the top value
            emissions_df = self.ref_db_emissions_df
            ingrd_co2 = emissions_df[emissions_df.ingredient == ingrd_name]['emissions'].values[0]

            co2 = round(ingrd['quantity'] * ingrd_co2, 2)
            total_co2 = round(total_co2,2) + co2
            ingrdList_co2.append({'ingredient' : ingrd_name, 'co2' : co2})

        return total_co2, ingrdList_co2
    
    def search_recipe_in_db(self, recipeName):
        # # Input : recipeName (str)
        # # OUTPUT(Tuple) : isExist (bool),
        #                   Total CO2 (str), 
        #                   Ingredient CO2 Information List
        #                   { "ingredient" : <str: Ingredient name>, "co2" : <float: CO2 emission> }
        engine = self.gcp_db_engine
        session = Session(engine)
        return True

    def get_ingrd_list(self):
        rs = self.ref_db_con.execute('SELECT distinct(ingredient) FROM emissions')

        ingrd_db = []
        for r in rs:
          ingrd_db.append(r[0])

        return ingrd_db

    def update_userhistory(self, recipeName, total_co2, ingrdList_co2):
        # # Input : recipeName (str),
        #           Total CO2, 
        #           Ingredient CO2 Information List
        #           { "ingredient" : <str: Ingredient name>, "co2" : <float: CO2 emission> }

        return 
    
    def update_nlpsimresult(self, update_history):
        # # Input : recipeName (str),
        #           Total CO2, 
        #           Ingredient CO2 Information List
        #           { "ingredient" : <str: Ingredient name>, "co2" : <float: CO2 emission> }

        for update in update_history:
            orig = update['orig']
            new = update['new']
            ins = users.insert().values(name="jack", fullname="Jack Jones")

        conn = self.gcp_db_con
        conn.execute(ins)
        return

