from datetime import datetime
from pytz import timezone

def utc(epoch_time):
    """
    Convert epoch time to UTC time
    """
    return datetime.fromtimestamp(epoch_time, tz=timezone.utc)
