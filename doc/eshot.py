import csv
import json
import sqlite3
import urllib.request
import ssl

print ("Getting latest data from source...")

def fetch_data_and_save(url):
    csv_filename = url.split('/')[-1]
    sslContext = ssl.create_default_context()
    try:
        csv_web = urllib.request.urlopen(url, context=sslContext)
    except urllib.error.URLError as e:
        print (e.reason)
        if (type(e.reason) == ssl.SSLCertVerificationError):
            sslContext.check_hostname = False
            sslContext.verify_mode = ssl.CERT_NONE
            print ("Trying again with unverified context...")
            csv_web = urllib.request.urlopen(url, context=sslContext)
        else:
            exit()
    dir = "./"
    with open(dir + csv_filename, 'wb') as f:
        f.write(csv_web.read())

    print ("Converting csv to json...")
    print(csv_filename.split('.'))
    json_filename = csv_filename.split('.')[0] + ".json"
    csvfile = open(dir + csv_filename, 'r')
    first_line = csvfile.readline() # get the header line
    fieldnames = first_line.split(';') # get the field names
    jsonfile = open(dir + json_filename, 'w')
    reader = csv.DictReader( csvfile, fieldnames, delimiter=';')
    out = json.dumps( [ row for row in reader ] )
    jsonfile.write(out)
    print ("%s bytes" % len(out) )
    print ("Done")

urls = ["https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-duraklari.csv",
        "https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-hareketsaatleri.csv",]

for url in urls:
    fetch_data_and_save(url)

connection = sqlite3.connect("eshot.db")
print(connection.total_changes)