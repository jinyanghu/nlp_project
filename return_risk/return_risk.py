import numpy as np
from pathlib import Path
import math
import pickle

def write_csv(file_name , file_list , c_list , cov=False):
  
  with open(file_name , 'a' , encoding='utf8') as wf:
    for i in range(len(c_list)):
      print_str = c_list[i] + ',' + str(file_list[i])[1:-2]
      print(print_str , file=wf)
  wf.close()  

def write_np(file_name , file):
  loc_file = str(Path.cwd()) + r'\\model\\'+file_name
  with open(loc_file , 'wb') as f:
    pickle.dump(file , f)
  f.close()      

file_type = '.csv'
company_list = ['富邦金',
        '國泰金',
        '台積電',
        '華碩',
        '亞泥',
        '南亞',
        '陽明',
        '華航']

return_list = []
for c in company_list:
  file_name = c + 'Y' + file_type
  c_return = []
  with open(str(Path.cwd())+r'\\year_growth_rate\\'+file_name , 'r') as f:
    for l in f.readlines():
      l = float(l.strip())
      c_return.append(l)
  f.close()   
  return_list.append(c_return)
 
return_list = np.array(return_list)

       
mean_list = np.round(np.mean(return_list , 1) , decimals=4)
var_list = np.round(np.var(return_list , 1 , ddof=1) , decimals=4)
std_list = np.round(np.std(return_list , 1 , ddof=1) , decimals = 4)
cov_mtx = np.round(np.cov(return_list) , decimals=4)


print(company_list)
print(np.mean(return_list , 1))
print(std_list)
print(np.var(return_list , 1 , ddof=1))
print(np.cov((return_list))) 

write_np('company.pickle' , company_list)
#write_np('return.pickle' , mean_list)
#write_np('risk.pickle' , var_list)
#write_np('cov.pickle' , cov_mtx)

print('Ratio: \n')
#print(np.round(mean_list / std_list , decimals=4))
x = np.array([0.1 , 0 , 0.36 , 0.04 , 0.3 , 0 , 0 , 0.2])
mean_list = np.round(np.mean(return_list , 1) , decimals=4)
print(mean_list.dot(x))

create_file = False
if create_file:
  write_csv('return.csv' , mean_list , company_list)
  write_csv('var.csv' , var_list , company_list)
  write_csv('cov.csv' , cov_mtx , company_list , cov=True)