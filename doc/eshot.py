import csv
import json
import urllib.request

print ("Getting latest data from source...")
duraklar_web = urllib.request.urlopen('https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-duraklari.csv')
with open('eshot-otobus-duraklari.csv', 'wb') as f:
    f.write(duraklar_web.read())

print ("Converting csv to json...")
csvfile = open('eshot-otobus-duraklari.csv', 'r')
jsonfile = open('eshot-otobus-duraklari.json', 'w')
fieldnames = ("DURAK_ID","DURAK_ADI","ENLEM","BOYLAM", "DURAKTAN_GECEN_HATLAR")
reader = csv.DictReader( csvfile, fieldnames, delimiter=';')
next(reader, None) # skip the header row
out = json.dumps( [ row for row in reader ] )
jsonfile.write(out)
print ("%s bytes" % len(out) )
print ("Done")
