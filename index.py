import sys, logging
sys.path.insert(0, "/home/ormiret/webapps/theme/htdocs/")
logging.basicConfig(stream=sys.stderr)
from picker import app as application
