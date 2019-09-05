

import datetime
def mk_caller_reference(name):
    """Make a unique caller reference so that each call to the API
    is different so we dont hit repeat problems """
    return name + datetime.datetime.utcnow()
