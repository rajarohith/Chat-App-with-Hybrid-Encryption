# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:15:15 2020

@author: RAJA ROHITH
"""
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 18:18:01 2020
"""
import sys
import sympy
import random
sys.setrecursionlimit(1000000)

#Computing the Extended Euclidean Algorithm (EEA) and return (g, x, y) a*x + b,*y = gcd(x, y)
def egcd( a ,b ):
    if a==0:
        return( b , 0 , 1 )
    else:
        g , x , y = egcd ( b % a , a )
        return( g , y - ( b // a) * x ,x)
def mulinv( b , n ):
    #The method will return the multiplicative inverse of b modulo n
    g,x,_ = egcd( b , n )
    if ( g == 1 ):
        return x % n
    else:
        sys.exit( "wrong input" )
#ascii_val is a list that will have all ascii values from 14 to 127
ascii_val=[]
for i in range(14,128):
    ascii_val.append(chr(i))
#chton is a dictionary for converting characters to integers and the values start from 1
chton = {}
x = 1
for i in ascii_val:
    chton[i] = x
    x += 1
#ntoch is another dictionary for converting integer number to its corresponding letter
ntoch = {}
for i in ascii_val:
    ntoch[chton[i]] = i
#Vigenere cipher is called first for the encryption
def vigencrypt(msg):
    key=""
    emsg=""
    #A random key is generated according to the length of message
    for i in range(len(msg)):
        k=random.choice(ascii_val)
        if(k==' '):
            i-=1
        else:
            key+=k
    #
    for i in range(len(msg)):
        x = (chton[msg[i]] + chton[key[i]]) % 114
        emsg+=ntoch[x]
    return [key,emsg]
#vigencrypt will return a list of key values and encrypted message
def encrypt(msg):
    #First do Vigenere cipher encryption
    msg1=vigencrypt(msg)
    key=msg1[0]
    msg=msg1[1]
    distinct = []
    #Take 4 random numbers
    p = sympy.randprime(10, 40)
    distinct.append(p)
    q = sympy.randprime(10, 40)
    while (q in distinct):
        q = sympy.randprime(10, 40)
    distinct.append(q)
    r = sympy.randprime(10, 40)
    while (r in distinct):
        r = sympy.randprime(10, 40)
    distinct.append(r)
    s = sympy.randprime(10, 40)
    while (s in distinct):
        s = sympy.randprime(10, 40)
    distinct.append(s)
    # The second step is to compute n,m the product of p & q and r & s. In our case:
    n = p * q
    m = r * s
    # Next, we need to compute the Euler totient function for n,m,N \phi(n) which is
    # defined as \phi(n) = (p-1)*(q-1):
    N = n * m
    phi_n = (p - 1) * (q - 1)
    phi_m = (r - 1) * (s - 1)
    phi_N = phi_n * phi_m
    # Now we have to chose an exponent e that is relatively prime to
    # phi(n) = (p-1)*(q-1). The pair (e, n) becomes our public key that we use
    # to encrypt messages.
    e = sympy.randprime(10, phi_N)
    while (e in distinct):
        e = sympy.randprime(10, phi_N)
    distinct.append(e)
    # The next step is to calculate the value d for our private key
    d = mulinv(e, phi_N)
    # The pair (d,n) becomes private key and is only known to the receiver
    # Inorder to use an extra key Mu we will need n1,m1 with which we will calculate n1_inverse
    # and m1_inverse
    n1 = N // n
    m1 = N // m
    # n1_inverse and m1_inverse are calculated using the multiplicative inverse method with the
    # help of extended euclids algorithm.
    n1_inv = mulinv(n1, n)
    m1_inv = mulinv(m1, m)
    # We need another values k1,k2 to calculate k1_inverse and k2_inverse which are used to calculate Mu
    k1 = sympy.randprime(10, 40)
    while (k1 in distinct):
        k1 = sympy.randprime(10, 40)
    distinct.append(k1)
    k2 = sympy.randprime(10, 40)
    while (k2 in distinct):
        k2 = sympy.randprime(10, 40)
    distinct.append(k2)
    # k1_inverse and k2_inverse are also calculated using the multiplicative inverse method
    k1_inv = mulinv(k1, n)
    k2_inv = mulinv(k2, m)
    # calculate mu according to the formula
    mu = ((k1 * n1 * n1_inv) + (k2 * m1 * m1_inv))
    mu = mu % N
    encrypt_string=str(k1_inv)+" "+str(n)+" "+str(d)
    cipher_text=[]
    for i in msg:
        #ct gets the cipher text value of the corresponding character
        ct = ( ( mu % N ) * ( ( chton[i] % N )**e ) ) % N
        #ct gets appended to the cipher_text list which is used for decryption
        cipher_text.append( ct )
        encrypt_string=encrypt_string+" "+str(ct)
    return key+" "+encrypt_string
#encrypt function will return the cipher text and this is stored in database
#vigdecrypt is called from decrypt function after RSA with CRt decryption is done
def vigdecrypt(key,dec_msg):
    dmsg=""
    for i in range(len(dec_msg)): 
        x = (chton[dec_msg[i]] - chton[key[i]]+ 114) % 114
        dmsg+=ntoch[x]
    return dmsg
#vigdecrypt will return the original message to decrypt function
#decrypt function is to perform decryption operation
def decrypt(dec_msg):
    dec_message=""
    ct=[]
    s=""
    j=0
    #
    for i in range(len(dec_msg)):
        if (dec_msg[i] == " "):
            ct.append(s)
            j=i
            s = ""
            break
        else:
            s += dec_msg[i]
    for i in range(j+1,len(dec_msg)):
        if (dec_msg[i] == " " or i == (len(dec_msg) - 1)):
            if (i == (len(dec_msg) - 1)):
                s += dec_msg[i]
            ct.append(int(s))
            s = ""
        else:
            s += dec_msg[i]
    key=ct[0]
    k1_in=ct[1]
    nn=ct[2]
    dd=ct[3]
    for i in range(4,len(ct)):
        dm = ( ( (  ct[i] * (k1_in % nn ) ) % nn )** dd ) % nn
        dec_message += str(ntoch[dm])
    #The corresponding character is added to the decrypt_message string
    #This is again decrypted using the Vigenere cipher decrypt function
    dec_message=vigdecrypt(key,dec_message)
    return dec_message
#This function will return original text
