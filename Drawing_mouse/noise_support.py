from talon import Module, actions, noise

noise_module = Module()

@noise_module.action_class
class NoiseActions:
    def noise_pop():
        """Invoked when the user does the pop noise."""
        pass

    def noise_hiss_start():
        """Invoked when the user starts hissing (potentially while speaking)"""
        pass

    def noise_hiss_stop():
        """Invoked when the user finishes hissing (potentially while speaking)"""
        pass

def pop_handler(blah):
    actions.user.noise_pop()

def hiss_handler(active):
    if active:
        actions.user.noise_hiss_start()
    else:
        actions.user.noise_hiss_stop()

noise.register("pop", pop_handler)
noise.register("hiss", hiss_handler)
