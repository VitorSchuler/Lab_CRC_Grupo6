import sys

def xor_bits(a, b):
    """
    Faz o XOR bit a bit entre duas strings.
    Ex: 101 XOR 110 = 011
    Retorna o resultado ignorando o primeiro bit (que sempre zera na divisão).
    """
    resultado = []
    for i in range(1, len(b)):
        if a[i] == b[i]:
            resultado.append('0')
        else:
            resultado.append('1')
    return "".join(resultado)

def calcular_crc_manual(dados_bits, gerador_bits):
    """
    Simula a divisão longa de binários.
    dados_bits: Mensagem (M)
    gerador_bits: Polinômio divisor (G)
    """
    r = len(gerador_bits) - 1
    
    mensagem_aumentada = list(dados_bits + '0' * r)
    
    for i in range(len(dados_bits)):
        if mensagem_aumentada[i] == '1':
            janela = mensagem_aumentada[i : i + len(gerador_bits)]
            resultado_xor = xor_bits(janela, gerador_bits)
            for j in range(len(resultado_xor)):
                mensagem_aumentada[i + j + 1] = resultado_xor[j]
                
    resto = "".join(mensagem_aumentada[-r:])
    return resto


if __name__ == "__main__":
    print("--- TESTE DE IMPLEMENTAÇÃO MANUAL DO CRC ---")
    
    dados_teste = "1101011111"  
    gerador_teste = "10011"    

    print(f"Mensagem: {dados_teste}")
    print(f"Gerador:  {gerador_teste}")
    
    crc = calcular_crc_manual(dados_teste, gerador_teste)
    
    print("-" * 30)
    print(f"CRC Calculado: {crc}")
    print("-" * 30)

    print(f"Quadro a transmitir: {dados_teste}{crc}")
