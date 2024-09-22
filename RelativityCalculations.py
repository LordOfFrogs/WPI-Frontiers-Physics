from vpython import *
#Web VPython 3.2

c = 3e+8

def dilated(t, v):
    return t / sqrt(1 - (v**2 / c**2) )
    
while True:
    t = input("Enter time (sec) (q to quit): ")
    if t == 'q':
        break
    
    v = input("Enter velocity (m/s) (q to quit): ")
    if v == 'q':
        break
    
    l = input("Enter length (m) (q to quit): ")
    if l == 'q':
        break
    
    try:
        dilatedT = dilated(float(t), float(v))
        dilatedL = dilated(float(l), float(v))
        print(f"Input: {t} sec, {l} meters, {v} m/s")
        print("Dilated time (sec): ", dilatedT)
        print("Dilated length (m): ", dilatedL)
    except ValueError:
        print("Please enter a number")
    except Exception as err:
        raise err
    print()