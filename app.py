from flask import Flask, render_template, request
import pyromat as pm
import numpy as np
# print(np.round(45.3456,2))
app = Flask(__name__)

# Define refrigerant properties using pyromat
refrigerant_properties = {
    # "R717": pm.get("ig.H3N"),
    "R134a": pm.get("mp.C2H2F4")
   }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    refrigerant = request.form['refrigerant']
    m = float(request.form['m'])  # mass flow rate in kg/s
    T1 = float(request.form['T1'])  # Evaporator temperature in K
    T3 = float(request.form['T3'])  # Condenser temperature in K

    # Retrieve refrigerant properties
    properties = refrigerant_properties.get(refrigerant)

    if properties is None:
        return "Error: Refrigerant properties not found."

    # Calculate enthalpy at different states
    # Assuming the correct method for enthalpy calculation is 'enthalpy'
                   # h1 = properties.enthalpy(T=T1)
  # Calculate enthalpy at different states
    #   Assuming this is the correct method for h3 calculation
     # s1 = properties.ss(T=T1)[1]
    # p_g = properties.ps(T=T3)
     # s2 = s1
    # T2 = properties.T_s(s=s2, p=p_g)
     # h2 = properties.h(T=T2, p=p_g)
     # h3 = properties.hs(p=p_g)[0]
     # h4 = h3    
    # # Calculate enthalpy at different states

    # h1 = properties.hs(T=T1)[0]
    # s1 = properties.ss(T=T1)[1]
    # p_g =properties.ps(T=T3)  
    # s2 = s1
    # T2 = properties.T_s(s=s2, p=p_g)
    # h2 = properties.h(T=T2,p=p_g)
    # h3 = properties.hs(p=p_g)[0]
    # s3 = properties.ss(p=p_g)[0]
    # h4 = h3
    # State 1 (Evaporator)
    h1 = properties.h(T=T1, x=1)  # Enthalpy of saturated liquid (hf) at T1
    s1 = properties.s(T=T1, x=1)  # Entropy of saturated liquid (sf) at T1
    # State 2 (Compressor)
    p_g = properties.ps(T=T3)  # Saturation pressure at T3
    s2 = s1  # Isentropic process, so entropy remains constant
    # h2 = properties.h(T=T3, p=p_g)  # Enthalpy of saturated vapor (hg) at T3
    # State 3 (Condenser)
    h3 = properties.h(T=T3, x=0)  # Enthalpy of saturated liquid (hf) at T3
    h3g=properties.h(T=T3,x=1)
    s3=properties.s(T=T3,x=1)#Entropy of saturated vapour (s3)
    # State 4 (Expansion Valve)
    h4 = h3  # Isenthalpic process, so enthalpy remains constant
    cpv=properties.cp(T=T3)
    e=2.718281828459045
    T2=T3*(e**((s2-s3)/cpv))
    # exp=(s2-s3)+cpv*log(T2/T3)
    # sat_T2 = solve(exp,T2)
    h2=(h3g)+(cpv*(T2-T3))
    #round off upto 3 decimal places
    
    h1=np.round(h1,3)
    h2=np.round(h2,3)
    h3=np.round(h3,3)
    h4=np.round(h4,3)
    T2=np.round(T2,3)
    s1=np.round(s1,3)
    s2=np.round(s2,3)
    s3=np.round(s3,3)



    # Calculate refrigeration effect (Q)
    Q=np.round((m*(h1 - h4)),3)
    # Calculate compressor work (W)
    
    W=np.round((m*(h2 - h1)),3)
    # Calculate actual COP
    cop=np.round((Q / W),3)
    # Ideal COP assuming reversible process
    # ideal_cop =np.round((T1/(T2-T1)),3)
    ideal_cop =np.round((T1/(T3-T1)),3)
    return render_template('result.html', refrigerant=refrigerant,m=m, T1=T1,T2=T2,T3=T3,
    h1=h1,h2=h2,h3=h3,h4=h4,s1=s1,s2=s2,s3=s3,Q=Q, W=W, cop=cop, ideal_cop=ideal_cop)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=80)

