"""
Factory module which returns instance of specific store
"""


from store.consul_store import ConsulStore


def get_store(store_name):
    '''
       Returns an instance of the specific store
    '''
    _instance = globals()[store_name]()
    return _instance
