
# !pip install PyPDF2
# !pip install pdfplumber

# sbi bank statement pdf to table

import pdfplumber
import pandas as pd
import numpy as np
# argparse
import sys


def sbi(pdf_file):
  pdf = pdfplumber.open(pdf_file)
  sb = []
  for i in range(0,len(pdf.pages)-1):
    table=pdf.pages[i].extract_table()
    sb.append(pd.DataFrame(table[1::],columns=table[0]))
    # pd.DataFrame(table[1::],columns=table[0])

  sbi_bank = pd.concat(sb).reset_index().drop(['index'],axis='columns')

  # remove extra unwanted strings
  sbi_bank['Description'] = sbi_bank.Description.str.replace('\n','')
  sbi_bank['Txn Date'] = sbi_bank['Txn Date'].str.replace('\n',' ')
  sbi_bank.columns = sbi_bank.columns.str.replace('\n',' ')
  sbi_bank['Value Date'] = sbi_bank['Value Date'].str.replace('\n',' ')
  sbi_bank['Ref No./Cheque No.'] = sbi_bank['Ref No./Cheque No.'].str.replace('\n','-')
  sbi_bank['Debit'] = sbi_bank['Debit'].replace({'':0,',':''},regex=True)
  sbi_bank['Credit'] = sbi_bank['Credit'].replace({'':0,',':''},regex=True)
  sbi_bank['Balance'] = sbi_bank['Balance'].replace({'':0,',':''},regex=True)
  sbi_bank['Debit'] = pd.to_numeric(sbi_bank['Debit'])
  sbi_bank['Credit'] = pd.to_numeric(sbi_bank['Credit'])
  sbi_bank['Balance'] = pd.to_numeric(sbi_bank['Balance'])
  # print(pdf_file)
  xl_name = pdf_file.split('\\')[-1].split('.')[0]
  xl_path = 'public/downloads/xlsx/'+xl_name+'.xlsx'
  sbi_bank.to_excel(xl_path)
  return xl_path #indian_bank

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
# indian bank statement pdf to table
def indian(pdf_file):
  # print('indian bank')
  pdf = pdfplumber.open(pdf_file)

  inb = []
  for i in range(0,len(pdf.pages)):
    table=pdf.pages[i].extract_table()
    if i == 0:
      inb.append(pd.DataFrame(table[2:-1:],columns=table[1]))

    if i != 0:
      inb.append(pd.DataFrame(table[1:-1:],columns=table[0]))

  indian_bank = pd.concat(inb).reset_index()
  indian_bank = indian_bank.drop(['index'],axis='columns')

  # remove extra unwanted strings
  indian_bank.columns = indian_bank.columns.str.replace('\n',' ')
  indian_bank['PARTICULARS'] = indian_bank['PARTICULARS'].str.replace('\n','')
  indian_bank['WITHDRAWALS'] = indian_bank['WITHDRAWALS'].replace({'-':0,',':''},regex=True)
  indian_bank['DEPOSIT'] = indian_bank['DEPOSIT'].replace({'-':0,',':''},regex=True)
  indian_bank['BALANCE'] = indian_bank['BALANCE'].replace({'-':0,',':''},regex=True)

  # convert string into respective datatype
  indian_bank['WITHDRAWALS'] = pd.to_numeric(indian_bank['WITHDRAWALS'])
  indian_bank['DEPOSIT'] = pd.to_numeric(indian_bank['DEPOSIT'])
  xl_name = pdf_file.split('\\')[-1].split('.')[0]
  # indian_bank.to_excel(xl_name+'.xlsx')
  xl_path = 'public/downloads/xlsx/'+xl_name+'.xlsx'
  # print('-----',xl_path)
  indian_bank.to_excel(xl_path)
  return xl_path #indian_bank

#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# kotak bank statement pdf to table

def kotak(pdf_file):
  with pdfplumber.open(pdf_file) as pdf:
      first_page = pdf.pages[0]
      rows = first_page.extract_words()

  for row in rows:
      if row['text'] == '#':
          x0 = row['x0']
          top = row['top']
      if row['text'] == 'OPENING':
          bottom = row['bottom']
      if row['text'] == 'BALANCE(₹)':
          x1 = row['x1']

  box = (x0, top, x1, bottom)

  # Now we can crop the page starting with Name/Company for our upper and left bound, to right of 'ST' and bottom of "Watson"
  with pdfplumber.open(pdf_file) as pdf:
      first_page = pdf.pages[0]
      page = first_page.crop(bbox=(box))  # (x0, top, x1, bottom)
      table = page.extract_table(table_settings={
          "vertical_strategy": "text",
          "horizontal_strategy": "text",
      })

  # Fill the blank rows by including only those rows that do not all equal blank strings
  table = [row for row in table if ''.join([str(i) for i in row]) != '']

  # datawise
  a,r = [],[]
  l,d,e = np.empty(len(table[1::][0]), dtype=object),np.empty(len(table[1::][0]), dtype=object),np.empty(len(table[1::][0]), dtype=object)
  c = 0
  for row in table[1:8]:
    if c < len(table[1:8])-1:
      if len(row[0]) != 0:
        a.append(a)
        l = [str(x) for x in row]
      else:
        d = [str(x) for x in row]
        if (len(l) != 0) and (len(d) != 0):
            r.append(np.array(l,dtype=object)+' '+np.array(d,dtype=object))
      c = c+1
    else:
        break

  kotak_bank = pd.DataFrame(r,columns = table[0:1:][0])#.drop([0],axis='rows')


  kotak_bank['VALUE'] = kotak_bank[['VALUE','DATE']].apply(lambda row: ' '.join(row.values.astype(str)), axis=1)
  kotak_bank.drop(['DATE'],axis='columns',inplace=True)
  kotak_bank.rename(columns = {"VALUE": "VALUE DATE"},inplace=True)

  # Update the column names
  xl_name = pdf_file.split('\\')[-1].split('.')[0]
  xl_path = 'public/downloads/xlsx/'+xl_name+'.xlsx'
  kotak_bank.to_excel(xl_path)
  return xl_path #indian_bank
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

# banks = {'sbi':'sbi.pdf','indian':'indian.pdf','kotak':'kotak.pdf','bob':'bob.pdf'}


# pdf_file = "sbi.pdf" # indian.pdf, kotak.pdf
# xl_name = pdf_file.split('\\')[-1].split('.')[0]


  # C:\Users\ashis\OneDrive\Desktop\websoham\programming\bank_statement_to_pdf\googleColab\sbi.pdf
  

def convert_to_excel(pdf_file):
    file_path=''
    try:
      if '-' in pdf_file:
        xl_name = pdf_file.split('-')[-1].split('.')[0]
        # print(xl_name)
      else:
        xl_name = pdf_file.split('-')[-1].split('.')[0]
      
      if xl_name == "sbi":
        file_path = sbi(pdf_file=pdf_file)
      elif xl_name == "indian":
        file_path = indian(pdf_file=pdf_file)
        # return file_path
      elif xl_name == "kotak":
        file_path = kotak(pdf_file=pdf_file)
      else: 
        print(f'Error: this pdf file cannot be converted')
    except Exception as e:
        print(f'\nError = {e}')
    
    return file_path
        
if __name__ == "__main__":
    # Check if a PDF file path is provided as a command-line argument
    if len(sys.argv) != 2:
        # print('Usage: python script.py <pdf_file_path>')
        sys.exit(1)

    # Get the PDF file path from the command line argument
    pdf_file_path = sys.argv[1]

    # Convert the data to an Excel file
    pathFile = convert_to_excel(pdf_file_path)
    print(pathFile)

    # return pathFile