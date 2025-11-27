import sys

# --- 1. FERRAMENTA BÁSICA: XOR ---
def xor_bits(a, b):
    """
    Faz o XOR bit a bit entre duas strings.
    Ex: 101 XOR 110 = 011
    Retorna o resultado ignorando o primeiro bit (que sempre zera na divisão).
    """
    resultado = []
    # Começamos do 1 porque o bit 0 sempre zera na divisão
    for i in range(1, len(b)):
        if a[i] == b[i]:
            resultado.append('0')
        else:
            resultado.append('1')
    return "".join(resultado)

# --- 2. O ALGORITMO CRC (Divisão Polinomial) ---
def calcular_crc_manual(dados_bits, gerador_bits):
    """
    Simula a divisão longa de binários.
    dados_bits: Mensagem (M)
    gerador_bits: Polinômio divisor (G)
    """
    # Grau do gerador (quantos zeros vamos adicionar)
    r = len(gerador_bits) - 1
    
    # Adiciona os r zeros no final da mensagem (M * 2^r)
    # Convertemos para lista para poder modificar os bits durante a conta
    mensagem_aumentada = list(dados_bits + '0' * r)
    
    # Loop da divisão
    # Percorremos apenas a parte dos dados originais
    for i in range(len(dados_bits)):
        # Só dividimos se o bit atual for 1
        if mensagem_aumentada[i] == '1':
            # Pega a "janela" de bits para dividir
            janela = mensagem_aumentada[i : i + len(gerador_bits)]
            
            # Faz a subtração (XOR)
            resultado_xor = xor_bits(janela, gerador_bits)
            
            # Substitui os bits na mensagem pelo resto parcial
            for j in range(len(resultado_xor)):
                mensagem_aumentada[i + j + 1] = resultado_xor[j]
                
    # O que sobrou no final (os últimos r bits) é o resto (o CRC)
    resto = "".join(mensagem_aumentada[-r:])
    return resto

# --- 3. TESTE DE VALIDAÇÃO  ---
if __name__ == "__main__":
    print("--- TESTE DE IMPLEMENTAÇÃO MANUAL DO CRC ---")
    
    # Exemplo do Slide da aula
    dados_teste = "1101011111"  
    gerador_teste = "10011"    

    print(f"Mensagem: {dados_teste}")
    print(f"Gerador:  {gerador_teste}")
    
    # Calcula
    crc = calcular_crc_manual(dados_teste, gerador_teste)
    
    print("-" * 30)
    print(f"CRC Calculado: {crc}")
    print("-" * 30)
    
    # Verifica se bate com a teoria
    # Se a lógica estiver certa, o quadro final é a mensagem + o CRC
    print(f"Quadro a transmitir: {dados_teste}{crc}")