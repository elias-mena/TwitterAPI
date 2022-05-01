def serializeDict(a) -> dict:
    """ Serialize BSON to dict
    """
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    """ Serialize List[BSON] to List[Dict]
    """
    return [serializeDict(a) for a in entity]
