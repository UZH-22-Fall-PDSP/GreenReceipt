import json
from numpy import True_
import pandas as pd

import sqlalchemy
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy.orm import Session
from sqlalchemy.orm import declarative_base
from sqlalchemy.dialects.postgresql import insert

import random
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


CO2_REF_DB = 'postgresql://readonly:!JjFlGMjREf53965EvE@35.228.50.60:5432/postgres'
CO2_GCP_DB = 'postgresql://postgres:postgres@34.163.206.28:5432/postgres'
TEST_DB = 'postgresql://postgres:postgres@localhost:5432/postgres'

Base = declarative_base()

class greenrecipe_db():

    def __init__(self):

        self.ref_db_engine = sqlalchemy.create_engine(TEST_DB)
        self.ref_db_con = self.ref_db_engine.connect()
        self.ref_db_emissions_df = pd.read_sql_table(
            "emissions",
            con=self.ref_db_engine,
            columns=['ingredient',
                    'emissions',
                    'category'],
        )

        self.gcp_db_engine = sqlalchemy.create_engine(TEST_DB)
        self.gcp_db_con = self.gcp_db_engine.connect()
        
        self.Userhistory = Table('userhistory', Base.metadata, autoload=True, autoload_with=self.gcp_db_engine)
        self.Nlpsimresult = Table('nlpsimresult', Base.metadata, autoload=True, autoload_with=self.gcp_db_engine)

    def search_ingrdCO2_total(self, ingrdList, verbose):
        # # INPUT(List of dictionary) : Ingredient Information List
        # #                              {'ingredient' : string, 'quantity' : float, 'unit' : string}
        # # OUTPUT(Tuple) : Total CO2, 
        #                   Ingredient CO2 Information List
        #                   { "ingredient" : <str: Ingredient name>, "co2" : <float: CO2 emission> }

        ea_CONSTANT = 500 # 1ea = 500g
        ml_to_g_CONSTANT = 1 # 1ml = 1g
        kg_to_g_CONSTANT = 1000 # 1kg = 1000g

        ingrdList_co2 = []
        total_co2 = 0
        for ingrd in ingrdList:

            ingrd_name = ingrd['ingredient']

            # NOTE [CORNER CASE] handle the case that many items with the same ingredient name e.g. 'corn'
            # For now, just return the top value

            emissions_df = self.ref_db_emissions_df
            ingrd_co2 = emissions_df[emissions_df.ingredient == ingrd_name]['emissions'].values[0]

            unit = ingrd['unit']
            if (unit == 'ml'):
                q = ingrd['quantity'] * ml_to_g_CONSTANT / kg_to_g_CONSTANT
                co2 = round(q * ingrd_co2, 7)
            elif (unit == 'g'):
                q = ingrd['quantity'] / kg_to_g_CONSTANT
                co2 = round(q * ingrd_co2, 7)
            elif (unit == 'ea'):
                q = ingrd['quantity'] * ea_CONSTANT / kg_to_g_CONSTANT
                co2 = round(q * ingrd_co2, 7)
            else: # kg or others
                q = ingrd['quantity']
                co2 = round(q * ingrd_co2, 7)

            total_co2 = round(total_co2,7) + co2
            ingrdList_co2.append({'ingredient' : ingrd_name, 'co2' : co2})

        if verbose: print(f"DONE - search ingredients in DB and calculate total co2")

        return total_co2, ingrdList_co2
    
    def search_recipe_in_db(self, recipeName, verbose = False):
        # # Input : recipeName (str)
        # # OUTPUT(Tuple) : isExist (bool),
        #                   Total CO2 (str), 
        #                   Ingredient CO2 Information List
        #                   { "ingredient" : <str: Ingredient name>, "co2" : <float: CO2 emission> }
        r = recipeName
        isExist = False
        total_co2 = 0
        ingrdList_co2 = []

        table = self.Userhistory
        with Session(self.gcp_db_engine) as session:
            select_stmt = table.select().with_only_columns([table.c.recipename, table.c.totalco2, table.c.ingrdlist]).where(table.c.recipename == r)
            result = session.execute(select_stmt).first()
            if result != None:
                isExist = True
                total_co2 = float(result['totalco2'])
                ingrdList_co2 = json.loads(result['ingrdlist'])
        
        if verbose: print(f"Done - {isExist}")

        return isExist, total_co2, ingrdList_co2

    def get_ingrd_list(self):
        rs = self.ref_db_con.execute('SELECT distinct(ingredient) FROM emissions')

        ingrd_db = []
        for r in rs:
          ingrd_db.append(r[0])

        return ingrd_db

    def get_cat_ingrd_list(self, category, verbose = False):
        # TODO: Tasks pending completion -@hyeongkyunkim at 11/15/2022, 1:15:53 PM
        # Get ingredient list of the category
        # dummy_name = category + id_generator(size = 3)
        # dummy_number = round(random.random(),7)

        cat = category

        emissions_df = self.ref_db_emissions_df
        cat_ingrd_co2 = emissions_df[emissions_df.category == cat][['ingredient','emissions']]
        cat_ingrd_co2_list = []
        for i, ingrd in cat_ingrd_co2.iterrows():
            _ = {'ingredient': ingrd['ingredient'],'co2': ingrd['emissions']}
            cat_ingrd_co2_list.append(_)

        if verbose: print(f"Done - search ingredients of {category} Total {len(cat_ingrd_co2_list)} ea")
        return cat_ingrd_co2_list

    def update_userhistory(self, recipeName, total_co2, ingrdList_co2, verbose = False):
        # # Input : recipeName (str),
        #           Total CO2, 
        #           Ingredient CO2 Information List
        #           { "ingredient" : <str: Ingredient name>, "co2" : <float: CO2 emission> }
        r = recipeName
        t = total_co2
        ingrds = json.dumps(ingrdList_co2)

        table = self.Userhistory
        with Session(self.gcp_db_engine) as session:
            insert_stmt = insert(table).values(recipename=r
                                                ,totalco2=t
                                                ,ingrdlist=ingrds)
            session.execute(insert_stmt)
            session.commit()

        if verbose: print("DONE - update userhistory DB")

        return True
    
    def update_nlpsimresult(self, update_history, verbose = False):
        # # Input : {'ingrd': orig_ingrd_name,
        #            'result':[(rank1_name, rank1_sim), (rank2_name, rank2_sim), (rank3_name, rank3_sim)]}
        table = self.Nlpsimresult
        with Session(self.gcp_db_engine) as session:
            for u in update_history:
                insert_stmt = insert(table).values(ingrd=u['ingrd']
                                                    ,result1=u['res'][0][0]
                                                    ,result1num=u['res'][0][1]
                                                    ,result2=u['res'][1][0]
                                                    ,result2num=u['res'][1][1]
                                                    ,result3=u['res'][2][0]
                                                    ,result3num=u['res'][2][1])
                do_nothing_stmt = insert_stmt.on_conflict_do_nothing(index_elements=['ingrd'])
                session.execute(do_nothing_stmt)

            session.commit()

        if verbose: print("DONE - update nlpsimresult DB")
        return True


