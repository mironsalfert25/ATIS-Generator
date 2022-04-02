from cgitb import text
import time
import os
import urllib

###################################################
key = 7a109fd5fcfb4cfb8cca8acab73e5199
###################################################

voiceUrl = "http://api.voicerss.org/?key=" + key + "&hl=en-gb&v=Harry&c=MP3&f=8khz_8bit_mono&src="

voiceTemplate = """{airport} INFORMATION {letter}, TIME {validTime} zulu.
DEPARTURE RUNWAY 18, ARRIVAL RUNWAY 18.
TRANSITION LEVEL FLIGHT LEVEL 1 5, SURFACE WIND VARIABLE.
VISIBILITY 10 KILOMETRES OR MORE.
TEMPERATURE PLUS 6, DEW POINT PLUS 5.
QNH 1 0 1 3 HECTOPASCALS.
ACKNOWLEDGE RECEIPT OF INFORMATION {letter}.
AND ADVISE AIRCRAFT TYPE ON FIRST CONTACT"""

textTemplate = """{airport} ATIS Information {letter}.
▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
Valid as of {validTime}z.

Airspace Ceiling: FL060

Departure Runway: {depRunway}
Arrival Runway: {arrRunway}
Max Taxi Speed: 25kts

Advise aircraft type on first contact and advise you have information {letter} onboard.

NOTAMS:
- Realistic emergencies are authorised.
- Providing top-down control over airspace.
- All aircraft must use latest charts (https://github.com/Treelon/ptfs-charts/tree/main/).
- CPDLC is avaliable (you may request and recieve IFR clearance in game chat)."""

#--airport name, letter, time, departure runway, arrival runway, letter

phoneticNumbers = {"0":"zero", "1":"one", "2":"two", "3":"tree", "4":"four", "5":"fife", "6":"six", "7":"seven", "8":"eight", "9":"niner"}
phoneticAlphabet = ["alpha", "bravo", "charlie", "delta", "echo", "foxtrot", "golf", "hotel", "india", "juliet", "kilo", "lima", "mike", "november", "oscar", "papa", "quebec", "romeo", "sierra", "tango", "uniform", "victor", "whiskey", "x-ray", "yankee", "zulu"]

specialPhonetics = {
    "R": "right",
    "L": "left",
    "C": "centre",
    " ": ""
}

print("ATIS Generator - Do not close this window if you want ATIS to be automatically generated every 30 minutes.")
print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")
airport = input("Airport Name: ")
departureRunway = input("Departure Runway: ").upper()
arrivalRunway = input("Arrival Runway: ").upper()
atisLetterCode = -1
atisLetter = "A"
textAtis = ""
voiceAtis = ""

if len(departureRunway) == 2:
    departureRunway = departureRunway + " "

if len(arrivalRunway) == 2:
    arrivalRunway = arrivalRunway + " "

voiceDepartureRunway = list(departureRunway)
voiceArrivalRunway = list(arrivalRunway)

print(voiceDepartureRunway[2])
L0 = phoneticNumbers[voiceDepartureRunway[0]]
L1 = phoneticNumbers[voiceDepartureRunway[1]]
L2 = specialPhonetics[voiceDepartureRunway[2]]
voiceDepartureRunway = L0 + " " + L1 + " " + L2

L0 = phoneticNumbers[voiceArrivalRunway[0]]
L1 = phoneticNumbers[voiceArrivalRunway[1]]
L2 = specialPhonetics[voiceArrivalRunway[2]]
voiceArrivalRunway = L0 + " " + L1 + " " + L2

def updateAtisLetter():
    global atisLetterCode
    global atisLetter
    atisLetterCode += 1

    if atisLetterCode > 25:
        atisLetterCode -= 26
      
    atisLetter = chr(65 + atisLetterCode)

def getTime():
    utcTime = time.gmtime()
    strHour = str(utcTime.tm_hour)
    strMin = str(utcTime.tm_min)

    if utcTime.tm_hour < 10:
        strHour = "0" + strHour

    if utcTime.tm_min < 10:
        strMin = "0" + strMin

    return strHour + strMin

def formatTextAtis():
    global textAtis
    atisTime = getTime()

    textAtis = textTemplate.format(airport = airport.title(), letter = atisLetter, validTime = atisTime, depRunway = departureRunway, arrRunway = arrivalRunway)
    print(atisTime + "z: Information " + atisLetter) 

def formatVoiceAtis():
    global voiceAtis
    atisTime = list(getTime())
    atisTime = phoneticNumbers[atisTime[0]] + " " + phoneticNumbers[atisTime[1]] + " " + phoneticNumbers[atisTime[2]] + " " + phoneticNumbers[atisTime[3]]

    voiceAtis = voiceTemplate.format(airport = airport, letter = phoneticAlphabet[atisLetterCode], validTime = atisTime, depRunway = voiceDepartureRunway, arrRunway = voiceArrivalRunway)

print("▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬")

while True:
    updateAtisLetter()
    formatTextAtis()
    formatVoiceAtis()

    file = open("ATIS.txt", "w", encoding="utf-8")
    file.write(textAtis)
    file.close()

    url = voiceUrl + urllib.parse.quote(voiceAtis)

    os.system("curl --silent \"" + url + "\" -H \"Pragma: no-cache\" ..... -H \"Cache-Control: no-cached\" > ATIS.mp3 ")
    os.system("start .")
    os.system("ATIS.txt")
    time.sleep(30 * 60)
