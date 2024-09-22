from vpython import *
#Web VPython 3.2
G = 6.674e-11
a_E=1.496e+11
a_M=2.2739e+11
m_S=1.989e+30
SECONDS_TO_DAYS = 1/86400
T_E=sqrt((4*pi**2) / (G*m_S) * a_E**3)
print("Earth's orbital period (days): ", T_E*SECONDS_TO_DAYS)

T_M=sqrt((4*pi**2) / (G*m_S) * a_M**3)
print("Mars's orbital period (days): ", T_M*SECONDS_TO_DAYS)

T_sat = sqrt((4*pi**2) / (G*m_S) * ((a_E+a_M)/2)**3)
print("Satellite time do mars (days): ", T_sat*SECONDS_TO_DAYS/2)

launch_deg = 180-T_sat/T_M*180
print("Degrees to launch at: ", launch_deg)

v_sat = sqrt((G*m_S) / ((a_E+a_M)/2))
print("Satellite speed (m/s): ", v_sat)

v_E = sqrt((G*m_S) / a_E)
print("Earth speed (m/s): ", v_E)

v_M = sqrt((G*m_S) / a_M)
print("Mars speed (m/s): ", v_M)