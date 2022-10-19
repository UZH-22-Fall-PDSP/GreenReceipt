from flask import Flask, request, jsonify
import greenrecipe

app = Flask(__name__)

@app.route('/get_co2_emissions', methods=['GET']) 
def get_co2_emissions():
    url = request.args.get('url')
    result = greenrecipe.get_co2_emissions(url)
    return '{}'.format(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port = 5000, debug = True)