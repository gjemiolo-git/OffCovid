import os
from flask import Flask, flash, redirect, render_template, request, session, url_for, send_from_directory

from urllib.request import urlopen as uReq
from urllib.parse import urlencode
from json import dumps
from requests import get

from bs4 import BeautifulSoup as soup


ENDPOINT = "https://api.coronavirus.data.gov.uk/v1/data"
AREA_TYPE = "nation"
AREA_NAME = "scotland"

filters = [
    f"areaType={ AREA_TYPE }",
    f"areaName={ AREA_NAME }"
]

structure = {
    "date": "date",
    "name": "areaName",
    "code": "areaCode",
    "dailyCases": "newCasesByPublishDate",
}


api_params = {
    "filters": str.join(";", filters),
    "structure": dumps(structure, separators=(",", ":")),
    "latestBy": "cumCasesByPublishDate"
}


formats = [
    "json",
    "xml",
    "csv"
]


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/favicon2.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon2.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
def index():
    perDayUK = covidPerDay()
    perWeekUK = covidPerWeek()
    perDayEH = covidEh(4)
    perWeekEH = covidEh(5)
    return render_template("index.html", perDayUK = perDayUK, perWeekUK = perWeekUK, perDayEH = perDayEH, perWeekEH = perWeekEH)

@app.route("/lateral")
def lateral():
    return render_template("lateral.html")

@app.route("/vaccination")
def vaccination():
    vfirstDose = firstDose()
    vsecondDose = secondDose()
    return render_template("vaccination.html", vfirstDose = vfirstDose, vsecondDose = vsecondDose)

@app.route("/pcr")
def pcr():
    return render_template("pcr.html")

@app.route("/help")
def help():
    return render_template("help.html")

@app.route("/precautions")
def precautions():
    return render_template("precautions.html")

def firstDose():
    url = "https://coronavirus.data.gov.uk/"
    client = uReq(url)
    page = client.read()
    client.close()

    newPage = soup(page, "html.parser")
    line = newPage.findAll("span", {"class" : "govuk-link--no-visited-state number-link"})[1].text
    value = ""
    write = False

    for character in line:
        if 47 < ord(character) < 58:
            write = True
        if write == True and (47 < ord(character) < 58 or ord(character) == 44):
            value += character
        elif write == False:
            pass
        else:
            return value

def secondDose():
    url = "https://coronavirus.data.gov.uk/"
    client = uReq(url)
    page = client.read()
    client.close()

    newPage = soup(page, "html.parser")
    line = newPage.findAll("span", {"class" : "govuk-link--no-visited-state number-link"})[3].text
    value = ""
    write = False

    for character in line:
        if 47 < ord(character) < 58:
            write = True
        if write == True and (47 < ord(character) < 58 or ord(character) == 44):
            value += character
        elif write == False:
            pass
        else:
            return value

if __name__ == "__main__":
    print(firstDose())


def covidPerDay():
    url = "https://coronavirus.data.gov.uk/"
    client = uReq(url)
    page = client.read()
    client.close()

    newPage = soup(page, "html.parser")
    line = newPage.find("span", {"class" : "govuk-link--no-visited-state number-link number"}).text
    value = ""
    write = False

    for character in line:
        if 47 < ord(character) < 58:
            write = True
        if write == True and (47 < ord(character) < 58 or ord(character) == 44):
            value += character
        elif write == False:
            pass
        else:
            return value

def covidPerWeek():
    url = "https://coronavirus.data.gov.uk/"
    client = uReq(url)
    page = client.read()
    client.close()

    newPage = soup(page, "html.parser")
    line = newPage.findAll("span", {"class" : "govuk-link--no-visited-state number-link"})[6].text
    value = ""
    write = False

    for character in line:
        if 47 < ord(character) < 58:
            write = True
        if write == True and (47 < ord(character) < 58 or ord(character) == 44):
            value += character
        elif write == False:
            pass
        else:
            return value
def getData():
    print(urlencode(api_params))

def covidEh(state):
    # If state == 4 - Per day
    # If state == 5 - Per Month
    url = "https://coronavirus.data.gov.uk/easy_read?postcode=EH6%208QS"
    client = uReq(url)
    page = client.read()
    client.close()

    newPage = soup(page, "html.parser")
    line = newPage.findAll("b", {"class" : ""})[state].text
    return(line)

def vaccinatedEdin():
    url = "https://coronavirus.data.gov.uk/easy_read?postcode=EH6%208QS#vaccinations"
    client = uReq(url)
    page = client.read()
    client.close()

    newPage = soup(page, "html.parser")
    line = newPage.findAll("b", {"class" : ""})[5].text
    return(line)


