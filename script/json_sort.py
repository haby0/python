"""
    使用递归对 json 格式数据做排序
"""

def generateQueryString(dict):
    List = []
    dict_param = {}
    dict_param = dict
    for key in dict_param.keys():
        traver("", key, dict_param[key], List)
    List.sort();
    queryString = ""
    for str in List:
        queryString = queryString + str
    return queryString


def traver(prexKeyPath, key, subValue, List):
    queryString = ""
    if isinstance(subValue, dict):
        subParam = {}
        subParam = subValue
        for subkey in subParam:
            traver(prexKeyPath + "-" + key, subkey, subParam[subkey], List)
    elif isinstance(subValue, list):
        subParam = []
        subParam = subValue
        for i in range(len(subParam)):
            if isinstance(subParam[i], list):
                traver(prexKeyPath, key, subParam[i], List)
            elif isinstance(subParam[i], dict):
                subsubParam = {}
                subsubParam = subParam[i]
                for subsubKey in subsubParam.keys():
                    traver(prexKeyPath + "-" + key, subsubKey, subsubParam[subsubKey], List)
            else:
                queryString = ""
                queryString = queryString + subParam[i]
                List.append(prexKeyPath + "-" + key + "-" + queryString + "  ")
    else:
        queryString = ""
        # queryString = queryString + str(subValue)
        queryString = queryString
        List.append(str(str(prexKeyPath) + "-" + str(key) + "-" + str(queryString) + "  "))
