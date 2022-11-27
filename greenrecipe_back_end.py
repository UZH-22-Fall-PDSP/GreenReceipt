from flask import Flask, request
import greenrecipe_total

"""
export FLASK_APP=greenrecipe_back_end.py
flask run --host=0.0.0.0 
"""

app = Flask(__name__)
grp = greenrecipe_total.greenrecipe()

@app.route('/recipeCO2', methods=['GET']) 
def get_recipe_co2_emissions():
    recipe = request.args.get('recipe')
    result = grp.get_recipe_co2_emissions(recipe, verbose = True) 
    return result

@app.route('/calculatorCO2', methods=['POST']) 
def get_ingrd_co2_emissions():
    if(request.data):
            jdata = request.get_json()
            ingrdList = {}
            ingrdList['ingrd'] = jdata['ingrd']
            ingrdList['ingrd_q'] = jdata['ingrd_q']
            ingrdList['ingrd_u'] = jdata['ingrd_u']
            result = grp.get_ingrd_co2_emissions(ingrdList, verbose = True) 
            return result
    else:
        return 'nothing'

@app.route('/simingrdset', methods=['GET']) 
def get_simingrdset_co2_emissions():
    ingrd = request.args.get('ingrd')
    print(type(ingrd))
    print(ingrd)
    result = grp.get_simingrdset_co2_emissions(ingrd, verbose = True) 
    return result

@app.route('/ingrdcat', methods=['GET']) 
def get_catingrdset_co2_emissions():
    cat = request.args.get('cat')
    result = grp.get_catingrdset_co2_emissions(cat, verbose = True) 
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)