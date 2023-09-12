def check_running(func):
    def wrapper(self, *args, **kwargs):
        if self.game_dictionary["game"]:
            return func(self, *args, **kwargs)
    return wrapper
