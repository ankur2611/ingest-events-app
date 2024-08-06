import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Add the handler to the logger
logger.addHandler(ch)
