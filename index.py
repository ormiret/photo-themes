import sys, logging
sys.path.insert(0, "/home/ormiret/webapps/ideas/htdocs/")
logging.basicConfig(stream=sys.stderr)
from cards_against_hackspace.web import app as application
