import numpy as np
from scipy.optimize import minimize
import pickle
from pathlib import Path



np.set_printoptions(suppress=True, threshold=1000)

class Model:

  def __init__(self , dim=8):
    self.file_list = ['return' , 'risk' , 'cov' , 'company']
    self.data_dict = {}
    self.preference = {'expect_return': 0.07, 
                   'fin_pr': 0.1,
                   'elec_pr': 0.5,
                   'trad_pr': 0.3,
                   'trans_pr': 0.2}
    self.load_data()
    print(self.data_dict['company'])
    self.weights = np.zeros(dim)
        
    '''
    for f in self.file_list:
      print(self.data_dict[f])      
    '''
  def load_data(self):
    for file in self.file_list:
      file_name = file + '.pickle'
      with open(file_name , 'rb') as f:
        self.data_dict[file] = pickle.load(f)
      f.close()                    
  
  def obj_function(self , x):
    return self.data_dict['cov'].dot(x).dot(x)

  def constraint1(self, x):
    return np.sum(x) - 1.

  def constraint2(self , x):
    return -x.dot(self.data_dict['return']) + self.preference['expect_return']   
  
  def constraint3(self , x , c_type):
    result = 0
    if c_type == 'fin_pr':
      result = x[0] + x[1] - self.preference[c_type]
    elif c_type == 'elec_pr':
      result = x[2] + x[3] - self.preference[c_type]
    elif c_type == 'trad_pr':
      result = x[4] + x[5] - self.preference[c_type]
    elif c_type == 'trans_pr':
      result = x[6] + x[7] - self.preference[c_type]

    return result 

  def constraint4(self , x):
    return -1*x - 0

  def constraint5(self , x):
    return x - 1

  def all_constraint(self, x):
    result = 0
    result += self.constraint1(x)**2 + max(self.constraint2(x),0)**2
    result += max(self.constraint3(x ,'fin_pr'),0)**2 + max(self.constraint3(x , 'elec_pr'),0)**2\
           + max(self.constraint3(x ,'trad_pr'),0)**2 + max(self.constraint3(x , 'trans_pr'),0)**2
    for v in x:
      result += max(self.constraint4(v),0)**2

    return result                     

  def violation(self , x):
    vio = 0
    con_value = []
    con_value.append(round(self.constraint1(x) , 4))
    con_value.append(round(self.constraint2(x) , 4))
    key = list(self.preference.keys())[1:]
    for k in key:
      con_value.append(round(self.constraint3(x, k) ,4))
    for v in x:
      con_value.append(round(self.constraint4(v),4))
    for value in con_value:
      if value > 0 :
        vio += 1    
    
    return vio    
      
      
    
  def penalty_func(self , x , mu):
    result = 0
    result = self.obj_function(x)
    result += mu *(1 * self.constraint1(x)**2 +(max(self.constraint2(x),0))**2)
    result += mu *(max(self.constraint3(x,'fin_pr'),0)**2 + max(self.constraint3(x,'elec_pr'),0)**2) 
    result += mu *(max(self.constraint3(x,'trad_pr'),0)**2 + max(self.constraint3(x,'trans_pr'),0)**2)
    result += mu *(max(self.constraint4(x[0]),0)**2 + max(self.constraint4(x[1]),0)**2 +\
            max(self.constraint4(x[2]),0)**2 + max(self.constraint4(x[3]),0)**2 +\
            max(self.constraint4(x[4]),0)**2 + max(self.constraint4(x[5]),0)**2 +\
            max(self.constraint4(x[6]),0)**2 + max(self.constraint4(x[7]),0)**2)
    return result                

  def barrier_func(self , x ,mu):
    result = 0
    result += self.obj_function(x) 
    result += mu *(-1/self.constraint2(x))
    result += mu *(-1/self.constraint3(x,'fin_pr') + -1 /self.constraint3(x,'elec_pr'))
    result += mu *(-1/self.constraint3(x,'trad_pr') + -1/self.constraint3(x,'trans_pr'))
    result += mu *(-1/self.constraint4(x[0]) + -1/self.constraint4(x[1])
                + -1/self.constraint4(x[2]) + -1/self.constraint4(x[3])
                + -1/self.constraint4(x[4]) + -1/self.constraint4(x[5])
                + -1/self.constraint4(x[6]) + -1/self.constraint4(x[7]))
    return result                 

  def penalty_method1(self , x0 , method , mu=0.1 , beta=1.5 , epoch=30):
    x = x0
    iteration = 1
    while iteration <= epoch:
      x = minimize(self.penalty_func, x, args=(mu) , method=method).x
      ans = self.obj_function(x)
      #print('Iteration: {} , Ans: {:3.4f}'.format(iteration , ans), np.round(x,decimals=4))
      mu = beta * mu 
      iteration += 1
    
    vio = self.violation(x)  
    #print('(Ans , x): {:3.4f}'.format(ans) , np.round(x , decimals=4) , np.round(np.sum(x)),
    #     'Violation: {}'.format(vio))
    #print('Expected return: {:3.4f}'.format(x.dot(self.data_dict['return'])))    
   
    return np.round(x , decimals=4) , round(ans , 4) , round(vio , 4)

  def penalty_method2(self , x0 , method ,mu=0.1 ,beta=1.5, eps=1e-3):
    x = x0
    iteration = 1
    while self.all_constraint(x) > eps:
      x = minimize(self.penalty_func, x, args=(mu) ,method=method).x
      ans = self.obj_function(x)
      #print('Iteration: {} , Ans: {:3.4f}'.format(iteration , ans), np.round(x,decimals=4))
      mu = beta * mu 
      iteration += 1
    
    vio = self.violation(x)  
    #print('(Ans , x): {:3.4f}'.format(ans) , np.round(x,decimals=4) , np.round(np.sum(x)),
    #      'Violation: {}'.format(vio))
    #print('Expected return: {:3.4f}'.format(x.dot(self.data_dict['return']))) 

    return np.round(x , decimals=4) , round(ans , 4) , round(vio , 4)

par_list = [(0.01,1.5) , (0.1,1.5) , (0.1,2)] #(0.5,4)
alg = ['BFGS' , 'Powell' , 'COBYLA']
ter_1 = [1e-3 , 1e-5 , 1e-8]
ter_2 = [10 , 25 , 50]
init_point = [np.ones(8) , 
              np.array([10,0,10,0,10,0,10,0]) , 
              np.array([0,0,0,2,2,2,1,1])]


title = ['beta_mu' , 'algorithm' , 'terminate' , 'init_point' , 
         'optimal_soultion', 'ans', 'violation']
def main(par_list , alg , ter_1 , ter_2 , init_point):
  sim = Model()
  result_list = []
  for p in par_list:
    for ag in alg:
      for x in init_point:

        for t1 in ter_1:
          #print(p , ag , x , t1)
          xf , ans , vio = sim.penalty_method2(x,ag,mu=p[0],beta=p[1],eps=t1)    
        
          result_list.append([p , ag , t1 , tuple(x) , tuple(xf) , ans , vio])  
        
        for t2 in ter_2:
          #print(p , ag , x , t2)
          xf , ans , vio = sim.penalty_method1(x,ag,mu=p[0],beta=p[1],epoch=t2)        
  
          result_list.append([p , ag , t2 , tuple(x) , tuple(xf) , ans , vio])          
  
  return result_list  

result_list = main(par_list , alg, ter_1,ter_2 , init_point)                          

result_file = 'exp.txt'
with open(result_file , 'w' ) as wf:
  print(str(title)[1:-1] , file=wf)
  for l in result_list:
    print_str = ''    
    for e in l:  
      print_str += str(e) + '\t'
    print_str = print_str[:-1]
    print(print_str , file=wf)        

