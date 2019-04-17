# Define common data structures.
import time

class NewsObject:

    # A news object in a structured way.
    def __init__(self, title, href, contents=None):
        self.title = title
        self.href = href # Use this as identifier.
        self.contents = contents # Holds whatever attributes that comes in.
        self.created_time = time.time() # remember created time.
        self.weight = 0

    @staticmethod
    def packContent(summary=None, content=None, timestamp=None, **kwargs):
        contents = {
            "summary": summary,
            "content": content,
            "timestamp": timestamp
        }
        if kwargs:
            contents.update(kwargs)
        return contents

    def calculate_weights(self):
        # TODO: somehow calculate an importance.
        pass
