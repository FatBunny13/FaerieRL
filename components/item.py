class Item:
    def __init__(self,item_id=None, use_function=None, targeting=False, targeting_message=None, **kwargs):
        self.item_id = item_id
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.function_kwargs = kwargs
