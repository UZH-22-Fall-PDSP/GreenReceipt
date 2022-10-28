

def ingrd_matching(ingrdList):
    # Input : <str: Ingredient Name>
    # Output : List [<str: Ingredient Name>, <str: Ingredient Matched>]
    ingrdList = [{'ingredient': 'peas', 'quantity': 1.0, 'unit': 'ea'}
            , {'ingredient': 'runner beans', 'quantity': 56.69, 'unit': 'g'}
            , {'ingredient': 'beef cold cuts', 'quantity': 14.79, 'unit': 'ml'}
            , {'ingredient': 'apple juice', 'quantity': 1.0, 'unit': 'ea'}
            , {'ingredient': 'peach', 'quantity': 59.14, 'unit': 'ml'}
            , {'ingredient': 'poppy seed', 'quantity': 14.79, 'unit': 'ml'}
            , {'ingredient': 'fish oil', 'quantity': 0.61, 'unit': 'ml'}
            , {'ingredient': 'celery', 'quantity': 0.61, 'unit': 'ml'}
            , {'ingredient': 'gem squash', 'quantity': 0.3, 'unit': 'ml'}
            , {'ingredient': 'sour cream', 'quantity': 0.3, 'unit': 'ml'}
            , {'ingredient': 'coconut', 'quantity': 29.57, 'unit': 'ml'}]
    return ingrdList

def ingrd_vectorCal():
    # Input : List [<str: Ingredient1>, ...]
    # Output : List [ {"name" : <str: Ingredient1>, "vector" : List[, ...]}, ... ]
    return