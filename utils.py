# Define common data structures.
import time

class NewsObject:

    # A news object in a structured way.
    def __init__(self, key, href, attributes=None, timestamp=None, summary=None):
        self.key = key # identify in dictionary. Use title for now.
        self.href = href
        self.attrs = attributes # Holds whatever attributes that comes in.
        self.created_time = time.time() # remember created time.
        self.timestamp = timestamp # Doesn't necessarily needs it.
        self.summary = summary
        self.weight = 0

    def calculate_weights(self):
        # TODO: somehow calculate an importance.
        pass
