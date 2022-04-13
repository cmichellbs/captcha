from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint

session = HTMLSession()

def get_all_forms(url):
    """Returns all form tags found on a web page's `url` """
    # GET request
    res = session.get(url)
    # for javascript driven website
    res.html.render()
    soup = BeautifulSoup(res.html.html, "html.parser")
    return soup.find_all("form-group")

r = get_all_forms('http://rais.gov.br/sitio/consulta_trabalhador_lista.jsf')