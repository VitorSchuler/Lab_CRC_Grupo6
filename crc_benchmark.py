import time
import tracemalloc
import os
import matplotlib.pyplot as plt
from crc import Calculator, Crc16

def xor_bits(a, b):
    resultado = []
    for i in range(1, len(b)):
        if a[i] == b[i]: resultado.append('0')
        else: resultado.append('1')
    return "".join(resultado)

def calcular_crc_manual(dados_bits, gerador_bits):
    r = len(gerador_bits) - 1
    mensagem_aumentada = list(dados_bits + '0' * r)
    for i in range(len(dados_bits)):
        if mensagem_aumentada[i] == '1':
            janela = mensagem_aumentada[i : i + len(gerador_bits)]
            resultado_xor = xor_bits(janela, gerador_bits)
            for j in range(len(resultado_xor)):
                mensagem_aumentada[i + j + 1] = resultado_xor[j]
    return "".join(mensagem_aumentada[-r:])

calculator_lib = Calculator(Crc16.MODBUS)
GERADOR_MODBUS_BIN = "11000000000000101" 

tamanhos_bytes = [1500, 4500, 9000]

dados_grafico = {
    "tamanho": tamanhos_bytes,
    "tempo_manual": [],
    "memoria_manual": [],
    "tempo_lib": [],
    "memoria_lib": []
}

print(f"{'TAMANHO':<10} | {'TEMPO MANUAL':<15} | {'TEMPO LIB':<15}")
print("-" * 45)

for tamanho in tamanhos_bytes:
    mensagem_bytes = os.urandom(tamanho)
    mensagem_bits = "".join(format(byte, '08b') for byte in mensagem_bytes)
    
    tracemalloc.start()
    inicio = time.perf_counter()
    
    _ = calcular_crc_manual(mensagem_bits, GERADOR_MODBUS_BIN)
    
    fim = time.perf_counter()
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    dados_grafico["tempo_manual"].append(fim - inicio)
    dados_grafico["memoria_manual"].append(pico / 1024) # KiB

    tracemalloc.start()
    inicio = time.perf_counter()
    
    _ = calculator_lib.checksum(mensagem_bytes)
    
    fim = time.perf_counter()
    _, pico = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    dados_grafico["tempo_lib"].append(fim - inicio)
    dados_grafico["memoria_lib"].append(pico / 1024) # KiB
    
    print(f"{tamanho:<10} | {dados_grafico['tempo_manual'][-1]:.5f}s        | {dados_grafico['tempo_lib'][-1]:.5f}s")

print("\nGerando gráficos comparativos...")

plt.figure(figsize=(10, 5))
plt.plot(tamanhos_bytes, dados_grafico["tempo_manual"], 'r-o', label='Manual (Lento)')
plt.plot(tamanhos_bytes, dados_grafico["tempo_lib"], 'b-x', label='Biblioteca (Rápido)')
plt.title('Comparativo de Tempo: Manual vs Biblioteca')
plt.xlabel('Tamanho da Mensagem (Bytes)')
plt.ylabel('Tempo (segundos)')
plt.legend()
plt.grid(True)
plt.savefig('grafico_crc_tempo.png')

plt.figure(figsize=(10, 5))
plt.plot(tamanhos_bytes, dados_grafico["memoria_manual"], 'r-o', label='Manual')
plt.plot(tamanhos_bytes, dados_grafico["memoria_lib"], 'b-x', label='Biblioteca')
plt.title('Comparativo de Memória: Manual vs Biblioteca')
plt.xlabel('Tamanho da Mensagem (Bytes)')
plt.ylabel('Pico de Memória (KiB)')
plt.legend()
plt.grid(True)
plt.savefig('grafico_crc_memoria.png')


print("Gráficos salvos como 'grafico_crc_tempo.png' e 'grafico_crc_memoria.png'.")
