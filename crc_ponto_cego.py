import random

# --- 1. CONFIGURAÇÕES PESSOAIS (Matrícula final 8) ---
SEU_NOME = "Vitor Schuler Velloso Borges" 
# Polinômio CRC-16/CCITT-FALSE (x^16 + x^12 + x^5 + 1)
POLINOMIO_GERADOR = "10001000000100001" 

def xor_bits(a, b):
    res = []
    for i in range(1, len(b)):
        res.append('0' if a[i] == b[i] else '1')
    return "".join(res)

def calcular_crc_manual(dados, gerador):
    r = len(gerador) - 1
    msg = list(dados + '0' * r)
    for i in range(len(dados)):
        if msg[i] == '1':
            janela = msg[i : i + len(gerador)]
            res_xor = xor_bits(janela, gerador)
            for j in range(len(res_xor)):
                msg[i + j + 1] = res_xor[j]
    return "".join(msg[-r:])

# --- 3. UTILITÁRIOS ---
def texto_para_bits(texto):
    return "".join(format(ord(c), '08b') for c in texto)

def introduzir_erro_rajada(quadro, tamanho_erro):
    """
    Inverte bits aleatórios para simular ruído
    """
    lista = list(quadro)
    pos = random.randint(0, len(quadro) - tamanho_erro)
    padrao = ""
    
    for i in range(pos, pos + tamanho_erro):
        lista[i] = '1' if lista[i] == '0' else '0' # Inverte
        padrao += "1"
        
    return "".join(lista), pos

if __name__ == "__main__":
    print(f"--- ANÁLISE DE PONTO CEGO (Matrícula Final 8) ---")
    print(f"Nome: {SEU_NOME}")
    print(f"Gerador: {POLINOMIO_GERADOR}")
    
    # Prepara a mensagem
    msg_bits = texto_para_bits(SEU_NOME)
    crc_orig = calcular_crc_manual(msg_bits, POLINOMIO_GERADOR)
    quadro_original = msg_bits + crc_orig
    
    print(f"\nCRC Original: {crc_orig}")
    print(f"Quadro (T): {quadro_original}")
    
    print("\n--- TESTE 1: Erros Aleatórios (O CRC deve detectar todos) ---")
    detectados = 0
    for i in range(1, 11):
        tam = random.randint(2, 20)
        quadro_sujo, pos = introduzir_erro_rajada(quadro_original, tam)
        
        resto = calcular_crc_manual(quadro_sujo, POLINOMIO_GERADOR)
        detectou = '1' in resto # Se resto != 000...000, detectou!
        
        status = "DETECTADO ✅" if detectou else "FALHA"
        if detectou: detectados += 1
        
        print(f"Teste {i}: Erro de {tam} bits na pos {pos}. Resultado: {status}")

    print(f"Total Detectados: {detectados}/10")
    
    print("\n--- TESTE 2: FORÇANDO O PONTO CEGO (Hacking) ---")
    print("Teoria: Se o erro for idêntico ao polinômio gerador, o resto da divisão será zero.")
    
    lista_hack = list(quadro_original)
    pos_ataque = 20 
    
    print(f"Injetando o padrão do gerador na posição {pos_ataque}...")
    
    for i in range(len(POLINOMIO_GERADOR)):
        bit_msg = lista_hack[pos_ataque + i]
        bit_poly = POLINOMIO_GERADOR[i]
        lista_hack[pos_ataque + i] = '0' if bit_msg == bit_poly else '1'
        
    quadro_ponto_cego = "".join(lista_hack)
    
    resto_hack = calcular_crc_manual(quadro_ponto_cego, POLINOMIO_GERADOR)
    detectou_hack = '1' in resto_hack
    
    print(f"Quadro Hackeado: {quadro_ponto_cego}")
    print(f"Resto calculado: {resto_hack}")
    
    if not detectou_hack:
        print("\n>>> SUCESSO! PONTO CEGO ENCONTRADO!  <<<")
        print("O CRC calculou resto 0, achando que a mensagem está íntegra, mas ela foi alterada.")
        print(f"Copie isso para a Entrega 4.2: Erro de padrão {POLINOMIO_GERADOR} na posição {pos_ataque}.")
    else:

        print("Algo deu errado no hack.")

