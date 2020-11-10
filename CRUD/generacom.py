import io
import re
import time
import PyPDF2
import requests
import pandas as pd
from bs4 import BeautifulSoup
import bs4
import os
print("bs4 version: " + bs4.__version__)

base_dir = os.getcwd()


def pjud(url, chunk_size = 30):
    print('pjud en accion')
    def leer_rol(url):
        pdf = requests.get(url) # verify = False solo si es necesario.
        pdf_bytes = io.BytesIO(pdf.content)
        pdf_lector = PyPDF2.PdfFileReader(pdf_bytes)
        contenido = pdf_lector.getPage(0).extractText().replace('\n','')
        rol = [re.findall(r'\d+-\d+',contenido, re.DOTALL|re.MULTILINE),url]
        return pd.DataFrame([rol])

    def chunks(lst, n):

        li = []
        for i in range(0, len(lst), n):
            li.append(lst[i:i + n])
        return li
    
    def publicaciones_judiciales(url, chunk_size = 30):
    
        df_ = pd.read_html(url)[0]

        page = requests.get(url)

        DOM = BeautifulSoup(page.content, 'html.parser').table

        expro = DOM.find(lambda x: x.text == "Expropiaciones")

        adop  = DOM.find(lambda x: x.text == "Adopciones")

        pdfs = DOM.find_all(lambda x: x.name == 'a' and "PDF" in x.text)
        #print(DOM)

        pdf_urls = [i['href'] for i in DOM.find_all(lambda x: x.name == "a" and "PDF" in x.text)]

        df = pd.DataFrame(pdf_urls, columns = ['pdf_url']).assign(sourceline = [i.sourceline for i in pdfs])
        #print(df)
        df_expro = df.set_index('sourceline').loc[expro.sourceline:adop.sourceline]

        expro_index = df_[df_[0] == 'Expropiaciones'].index[0]
        adop_index = df_[df_[0] == 'Adopciones'].index[0]

        df__ = df_.loc[expro_index:adop_index]
        df__ = df__[df__[0].apply(lambda x: len(x)>1 and x not in ['Expropiaciones', 'Adopciones'])]


        df__ = df__.assign(Link = df_expro.values)

        df__.columns = ['Titulo', 'Ver_pdf', 'Link']

        print(df__)
        return df__

    pjud = publicaciones_judiciales(url, chunk_size)
    
    url_list = pjud['Link']

    url_chunks = chunks(url_list, chunk_size)

    lo = pd.DataFrame([])

    for chunk in url_chunks:
        time.sleep(1)
        for url in chunk:

            lo = lo.append(leer_rol(url))
    
    lo.columns = ['rol_scan', 'Link']

    final = lo.merge(pjud, on = "Link")
    print(final)
    final.to_excel(f"{base_dir}/export/consulta.xlsx", index = False)
    
    return final

def hola(url):

    print("url_es" + str(url))
    return "url_es" + str(url) 