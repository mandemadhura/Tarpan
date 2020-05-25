"""
Factory module which returns instance of specific store
"""


from store.consul_store import ConsulStore


def get_store(store_name):
    '''
       Returns an instance of the specific store
    '''
    try:
        _instance = globals()[store_name]()
        return _instance
    except KeyError as key_error:
        print(f'No Module: {store_name} exist')
    except Exception as err:
        print(f'Problem occured while getting the instance \
              of the store: {err}')

