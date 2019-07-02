import jsonActions

def getParam(request,key,alternateValue):
    try:
        data = json.loads(request.get_data())
        if key in data:
            return data[key]
        else:
            return alternateValue
    except Exception:
        try:
            val = request.values.get(key)
            if val not in [None,""]:
                if jsonActions.jsonValid(val):
                    return jsonActions.jsonOut(val)
                else:
                    return val
            else:
                return alternateValue
        except Exception:
            return alternateValue
