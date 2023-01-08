import logging
import requests

# Set up the logger
logger = logging.getLogger("remote_logger")
logger.setLevel(logging.INFO)

# Set up the handler for the logger
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(handler)

# Set the URL of the log receiver
url = "http://localhost:8080/log"

# Define a custom logging handler that sends log messages to the log receiver
class RemoteLoggingHandler(logging.Handler):
    def emit(self, record):
        # Create the log message
        log_entry = self.format(record)

        # Send the POST request to the log receiver
        try:
            response = requests.post(url, json={"message": log_entry})
            response.raise_for_status()
        except Exception:
            self.handleError(record)

# Add the custom logging handler to the logger
remote_handler = RemoteLoggingHandler()
logger.addHandler(remote_handler)

# Test the logger
logger.info("This is a test log message")