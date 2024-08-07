import csv
import numpy as np

def can_multiply(A, B):
    return A.shape[1] == B.shape[0]


a = np.loadtxt(open('a.csv', "r"), delimiter=';')
M = np.loadtxt(open('M.csv', "r"), delimiter=';')
N = np.loadtxt(open('N.csv', "r"), delimiter=';')
MN_original = np.loadtxt(open('MN.csv', "r"), delimiter=';')

if can_multiply(M, N):
    MN = np.dot(M, N)
    print("M * N:")
    print(MN)
else:
    print("Não foi possível realizar a operação MN");    

if can_multiply(a.reshape(1, 10), M):
    aM = np.dot(a, M)
    print("a * M:")
    print(aM)
else:
    print("Não foi possível realizar a operação aM");    

if can_multiply(M, a):
    Ma = np.dot(M, a)
    print("M * a:")
    print(Ma)
else:
    print("Não foi possível realizar a operação Ma");    
