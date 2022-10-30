from flask import Flask, request, jsonify
import greenrecipe_total

"""
export FLASK_APP=greenrecipe_back_end.py
flask run --host=0.0.0.0 
"""


app = Flask(__name__)
grp = greenrecipe_total.greenrecipe()

@app.route('/recipeCO2', methods=['GET']) 
def get_co2_emissions():
    recipe = request.args.get('recipe')
    result = grp.get_co2_emissions(recipe, verbose = False) 
    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)