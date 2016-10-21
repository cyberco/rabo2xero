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
    if len(sys.argv) is not 2:
        print 'ERROR: provide a full path to the csv file as the first argument, and the output file as the second'
        return
    with open(sys.argv[1], 'rt') as input_file, open(sys.argv[2], 'wt') as output_file:
        reader = csv.reader(input_file)
        writer = csv.writer(output_file, quoting=csv.QUOTE_ALL)
        xero = collections.OrderedDict()
        for row in reader:
            print row
            if len(row) != 19:
                continue
            # if debit tx inverse amount
            if row[3] == 'D':
                row[4] = '-' + row[4]
            xero['date'] = row[7]
            xero['amount'] = row[4]
            xero['payee'] = row[6]
            # 'reference' is END_TO_END_ID (SEPA Credit Transfer)
            xero['reference'] = row[16]
            xero['description'] = ''.join(row[10:16])
            xero['transaction_type'] = row[8]
            writer.writerow(xero.values())

if __name__ == '__main__':
    main()
