import io

import pandas as pd
import requests
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from PyPDF2 import PdfReader

service_obj = Service('/chromedriver.exe') #path to file
driver = webdriver.Chrome(service = service_obj)

def writeToFile(id, text):
    f = open(id + '.txt', 'a')
    f.write(text)
    f.close()

def parsePDF(url, id):
    response = requests.get(url)
    a = ' '
    with io.BytesIO(response.content) as f:
        pdf = PdfReader(f)
        for page in pdf.pages:
            a = a + page.extract_text()
    return a

def parse(url, id):

    if (url.endswith('.pdf')):
        writeToFile(id, parsePDF(url, id))
        return

    driver.get(url)
    writeToFile(id, driver.find_element(By.XPATH, "/html/body").text)

if __name__ == '__main__':
    data = pd.read_csv('unique_ids_with_links - unique_ids_with_links.csv')
    for i in range(0, 998):
        parse(data.iloc[i]['Privacy link'], data.iloc[i]['ID'])
        print(data.iloc[i]['ID'])

