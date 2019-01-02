class Skill:
    def __init__(self, use_function=None, targeting=False, targeting_message=None,cooldown=None, **kwargs):
        self.use_function = use_function
        self.targeting = targeting
        self.targeting_message = targeting_message
        self.cooldown = cooldown
        self.function_kwargs = kwargs
