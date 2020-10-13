'''
LABORATORIO 4: MODULACION DIGITAL

Estudiante: Francisco Rousseau
Ayudante: Nicole Reyes
Profesor: Carlos Gonzalez
'''

######################## LIBRERIAS ########################
import matplotlib.pyplot as plt
import numpy as np


######################## FUNCIONES ########################

# Se encarga de realizar la modulacion FSK.
#
# Entrada: 
#   bits            - senal compuesta por bits
#   bitrate         - tasa de bit
#
# Salida:
#   tiemposenal     - tiempo de la senal modulada
#   senal           - senal obtenida por la modulacion
#   largobit        - largo de la senal modulada

def FSK(bits, bitrate):
    senal = []
    f1 = bitrate
    f2 = 2 * f1
    periodo = 1 / f1
    print("Frecuencia 0: ", f1,"\nFrecuencia 1: ", f2)
    
    largobit = int(periodo * 10 * f2) 
    tiempo = np.linspace(0, periodo, num = largobit)
    print("Num muestras en 1 bit: ", largobit)
    
    cero = np.cos(2 * np.pi * f1 * tiempo)
    uno = np.cos(2 * np.pi * f2 * tiempo)
    for bit in bits:
        if bit == 0:
            senal.extend(cero)
        else:
            senal.extend(uno)

    tiempoT = len(bits) * periodo  
    tiemposenal = np.linspace(0, tiempoT, len(senal))
    
    print("Tiempo total de la senal: ", tiempoT)
    print("Numero de muestras de la senal: ", len(senal), "\n")
    return tiemposenal, senal, largobit

# Se encarga de realizar la demodulacion FSK.
#
# Entrada: 
#   tiempo          - tiempo de bit
#   senal           - senal
#   largobit        - numero de muestra que tiene un bit
#   bitrate         - tasa de bit
#
# Salida:
#   bitsdemod    - senal demodulada, arreglo de bits
def DFSK(tiempo, senal, largobit, bitrate):
    f1 = bitrate
    f2 = 2 * f1
    cosf1 = np.cos(2 * np.pi * f2 * tiempo)
    dembit1 = senal * cosf1
    
    n_bits = int(len(dembit1) / largobit)
    bitsdemod = [] 
    
    for i in range(1, n_bits + 1):
        voltaje = dembit1[((i - 1) * largobit): i * largobit - 1]
        mediaV = np.mean(voltaje)
        
        if mediaV > 0.25:
            bitsdemod.append(1)
        else:
            bitsdemod.append(0)

    return bitsdemod



# Se encarga de aregar el ruido AWGN
#
# Entrada: 
#   senal           - senal
#   snr             - numero de muestra que tiene un bit
#
# Salida:
#   awgn         - senal con ruido agregado
def ruido(senal, snr):
    ruido = np.random.normal(0, 1, len(senal))
    energia_s = np.sum(np.abs(senal) * np.abs(senal))
    energia_n = np.sum(np.abs(ruido) * np.abs(ruido))
    snr_lineal = np.exp(snr/10)
    sigma = np.sqrt(energia_s / (energia_n * snr_lineal))
    print('Desviacion ruido: ' + str(sigma))
    ruido = sigma * ruido
    awgn = senal + ruido
    return awgn

# Se encarga de calcular la la tasa de error binario​ en una senal digital demodulada.
#
# Entrada: 
#   bitsdemod       - senal demodulada
#   bits            - senal
#
# Salida:
#   ber             - tasa de error
def error(bitsdemod, bits):
    contador = 0
    for i in range(len(bits)):
        if bits[i] != bitsdemod[i]:
            contador += 1
    print("Numero de errores en la transmision: ",contador)
    ber = float(contador / len(bits))
    print("Error rate: ",ber)
    return ber

# Se encarga de simular el canal con ruido
#
# Entrada: 
#   bitsrate       - tasa de bit
def simulacionCanal( bitrate ):
    largosenal = 1e5
    bits = np.random.randint(2, size = int(largosenal))
    colores = ['-b', '-g', '-r']
    
    plt.figure(1)
    for i in range(0, 3):
        snr_x = []
        ber_y = []
        bitrate = bitrate + i*1000 
        tiempo, senal, len_bit = FSK(bits, bitrate)
        
        for snr in range(-2, 12, 1):
            print("##### Prueba SNR = {}[dB] para bitrate = {}[bits/s] #####".format(snr, bitrate))
            awgn = ruido(senal, snr)
            demod = DFSK(tiempo, awgn, len_bit, bitrate) 
            ber = error(demod, bits)
            snr_x.append(snr)
            ber_y.append(ber)
            lab = str(bitrate) + ' [bps]'
            print("##### Fin prueba #####\n")
            
        plt.plot(snr_x, ber_y, colores[i], label=lab, marker="o")

    plt.grid(True)
    plt.xlabel('SNR (dB)')
    plt.ylabel('BER')
    plt.yscale('log')
    plt.xscale('linear')
    plt.title('Rendimiento SNR vs Bitrate')
    plt.legend()
    plt.show()


######################## MAIN ########################

print('Laboratorio N° 4\nBits de prueba:')
bits = [0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1]
print(bits)
print('Bitrate de prueba:')
bitrate = 100
print(bitrate)
print('...Aplicando modulacion FSK...')
time, senal, largobit = FSK(bits, bitrate)
print('...Obteniendo Grafico Senal Modulada...')
plt.plot(time,senal)
plt.show()
print('...Aplicando de-modulacion FSK...')
demod = DFSK(time, senal, largobit, bitrate)
print('Bits de Salida:')
print(demod)

print('TESTING FINALIZADO\n\nCOMENZANDO SIMULACION DE CANAL AWGN')
print('** Las imagenes solo se muestran, no se almacenan **')

bitrate = 1000
simulacionCanal(bitrate)


