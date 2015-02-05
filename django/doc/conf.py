import sys
import os
sys.path.insert(0, os.path.abspath('..'))
from django.conf import settings
settings.configure()

extensions = [
#    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinxcontrib.httpdomain',
]
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = 'Photo Server'
copyright = '2015, Return to the Source'
version = '0.1'
release = '0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_theme = 'default'
html_static_path = ['_static']
html_show_copyright = False
htmlhelp_basename = 'PhotoServerdoc'

