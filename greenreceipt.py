import greenreceipt_db as db
import greenreceipt_nlp as nlp
import greenreceipt_web as web



def get_co2_emissions(url):

    html = web.scrap_receipt(url)
    ingrds = web.parsing_ingredient(html)

    co2sum = 0
    totalresult = []
    for ingrd in ingrds:
        result = db.search_ingredCO2(ingrd)
        if result['emissions'] == None:
            newName = nlp.ingred_matching(ingrd['name'])[1]
            newIngrd = {'name':newName}
            ingrd.update(newIngrd)
            result = db.search_ingredCO2(ingrd)
        co2sum += result['emissions']
        totalresult = totalresult.append(result)

    db.update_user_request()
    
    return 