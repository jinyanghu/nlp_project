import numpy as np
import math
from pathlib import Path 


file_type = '.csv'
company_list = ['國泰金',
        '富邦金',
        '亞泥',
        '南亞',
        '台積電',
        '華碩',
        '陽明',
        '華航']

def to_annual(company_list , file_type):
  for c in company_list:
    year_growth = []  
    read_file = c + file_type
    with open(str(Path.cwd()) + r'\\season_growth_rate\\'+read_file , 'r') as f:        
      line_counter = 0
      year_rate = 1.0
      for l in f.readlines():
        l = float(l.strip())
        if (line_counter+1) % 4 != 0:
          year_rate *= (1+l)
        else:  
          year_growth.append(year_rate - 1)
          year_rate = 1.0
        line_counter += 1  
    f.close()
    
    dividend_file = c +'D'+file_type
    with open(str(Path.cwd()) + r'\\dividend\\'+dividend_file, 'r') as f:
      line_counter = 0
      for l in f.readlines():
        l = l.strip().split(',')
        dd_rate = float(l[-1]) / 100
        year_growth[line_counter] += dd_rate
    f.close()          
    
    write_name = c +'Y'+ file_type
    with open(str(Path.cwd()) + r'\\year_growth_rate\\'+write_name , 'w') as w:
      for r in year_growth:
        print(round(r ,4) , file=w)
    w.close()                          

def pure_season_growth(company_list , file_type): 
  for c in company_list:
    growth_list = []
    with open(c+file_type , 'r') as f:
      for l in f.readlines():
        l = l.strip().split('\t')
        for e in l:
          if not e[0].isdecimal() or e == '0':
            #print(e)  
            growth_list.append(float(e))    
    f.close()
  
    print(len(growth_list))  
    for i in range(len(growth_list)):
      if (i+1) % 2 != 0:
        growth_list[i] = None        
  
    write_file =  str(Path.cwd()) + r'\\season_growth_rate\\' + c + '.csv'
    with open(write_file , 'w' , encoding='utf8') as w:
      for r in growth_list:
        if r is not None:
          r = r / 100    
          print(round(r , 4) , file=w)
    w.close()            


to_annual(company_list , file_type)