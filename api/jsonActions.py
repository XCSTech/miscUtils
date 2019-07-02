from decimal import Decimal
import datetime
import json


def jsonOut(data):
    return json.dumps(jsonClean().encode(data))

class jsonClean(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        elif type(obj) == datetime.datetime:
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif type(obj) == datetime.date:
            return obj.strftime('%Y-%m-%d')
        else:
            return super(jsonClean, self).default(obj)

def jsonValid(data):
    try:
        json.dumps(data)
    except Exception:
        return False
    else:
        return True
