"""
Tool to convert Rabobank's bank statement CSV files to a format XERO can process.

Rabobank's format:
https://www.rabobank.nl/images/formaatbeschrijving_csv_kommagescheiden_nieuw_29539176.pdf

Xero's format:
https://help.xero.com/int/#BankImportCSVPrecodedi

Inspiration:
https://github.com/YY-/rabo-to-xero/blob/master/rabo_to_xero.php

"""
import sys
import collections
import csv

def main():
    if len(sys.argv) != 3:
        print 'ERROR: provide a full path to the csv file as the first argument, and the output file as the second'
        return
    with open(sys.argv[1], 'rt') as input_file, open(sys.argv[2], 'wt') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        xero = collections.OrderedDict()
        for row in reader:
            if len(row) != 26:
                continue
            xero['date'] = row[4]
            xero['amount'] = row[6].replace(',', '.')
            xero['payee'] = row[9]
            # 'reference' is END_TO_END_ID (SEPA Credit Transfer)
            xero['reference'] = row[15]
            xero['description'] = ''.join(row[19:22])
            print xero.values()
            writer.writerow(xero.values())

if __name__ == '__main__':
    main()
