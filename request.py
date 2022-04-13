from bs4 import BeautifulSoup

from pprint import pprint
from urllib.parse import urljoin
import webbrowser
import sys

from form_extractor import get_all_forms, get_form_details, session


details = get_form_details(get_all_forms('http://rais.gov.br/sitio/consulta_trabalhador_lista.jsf')[1])

pprint(details)