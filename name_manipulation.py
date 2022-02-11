# %%
import time

def get_timestamp_name(t_secs, ext):
    """Create a timestamp name."""
    timestamp =  time.strftime("%Y%m%d-%H%M%S", time.gmtime(t_secs))
    return timestamp + ext

def add_duplication_tag(num):
    """Wrap int into duplication string identifier."""
    return "-(#" + str(num) + ")"
# %%
