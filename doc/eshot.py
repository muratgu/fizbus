import csv
import json
import sqlite3
import urllib.request
import ssl

dir = "./"


def urlTryOpen(url):
    sslContext = ssl.create_default_context()
    try:
        return urllib.request.urlopen(url, context=sslContext)
    except urllib.error.URLError as e:
        print (e.reason)
        if (type(e.reason) == ssl.SSLCertVerificationError):
            sslContext.check_hostname = False
            sslContext.verify_mode = ssl.CERT_NONE
            print ("Trying again with unverified context...")
            return urllib.request.urlopen(url, context=sslContext)
        else:
            return None

def fetch_data_and_save(schema):
    url = schema['url']
    print('Fetching data from %s' % url)
    csv_filename = url.split('/')[-1]
    schema['csv_filename'] = csv_filename

    csv_web = urlTryOpen(url)
    if csv_web == None:
        print("Cannot connect. Will use existing file if exists.")
    else:
        with open(dir + csv_filename, 'wb') as f:
            f.write(csv_web.read())

    print("Looking for %s" % csv_filename)
    json_filename = csv_filename.split('.')[0] + ".json"
    try:
        csvfile = open(dir + csv_filename, 'r')
        print ("Found csv file, converting to json.")
        first_line = csvfile.readline() # get the header line
        fieldnames = first_line.strip().split(';') # get the field names
        if len(first_line) < 10 or len(fieldnames) < 1:
            print("Failed to read the csv file, cannot continue.")
            exit(-1)
        schema['col_names'] = fieldnames
        jsonfile = open(dir + json_filename, 'w')
        reader = csv.DictReader( csvfile, fieldnames, delimiter=';')
        out = json.dumps( [ row for row in reader ] )
        jsonfile.write(out)
        print ("%s bytes written as json." % len(out) )
    except IOError as e:
        print ("I/O Error, cannot continue")
        exit(-1)

def populate_db(schema):
    table_name = schema['table_name']
    csv_filename = schema['csv_filename']
    col_names = schema['col_names']

    print("Populating table [%s] from [%s]" % (table_name, csv_filename))

    try: 
        conn.execute(
            'drop table %s' % table_name
            )
    except: 
        pass
    finally:
        conn.execute(
            'create table %s(%s)' % (table_name, ','.join(col_names)) 
            )
        with open(dir + csv_filename, 'r') as f:
            reader = csv.DictReader( f, col_names, delimiter=';')
            next(reader) #skip header
            for row in reader:
                try:
                    conn.execute(
                        'insert into %s(%s) values(?,?,?,?,?)' % (table_name, ','.join(col_names)), 
                        [v for v in row]
                        )
                except Exception as e:
                    print("Cannot insert row")
                    print(row)
                    print(e)
                    exit(-1)
        row_count = conn.execute(
            'select count(*) from %s' % table_name
            ).fetchone()
        print('%s rows added' % row_count)

schemas = [
    {
        'url': 'https://openfiles.izmir.bel.tr/211488/docs/eshot-otobus-duraklari.csv',
        'table_name': 'duraklar',
    },
]

conn = sqlite3.connect("eshot.db")

print ("Getting latest data from source...")

for schema in schemas:
    fetch_data_and_save(schema)
    populate_db(schema)



