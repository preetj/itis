import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/IT_Infra_Project")

from main import app as application
