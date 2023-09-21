#Aqui vocês irão colocar seu algoritmo de aprendizado
import random
import connection as cnt
import time
# Declarações iniciais
alpha =  0.1
gamma = 0.9
epsilon = -0.9
eps = 2000

# Função para pegar a Qtable
def ler_qtable_de_arquivo():
    qtable = []

    with open('resultado.txt', 'r') as arquivo:
        for linha in arquivo:
            valores = linha.strip().split(' ')
            qtable.append([float(valor) for valor in valores])

    return qtable

# Função que faz o caminho contrario, escreve a Qtable alterado no resultado.txt
def salvar_qtable(qtable):
    with open('resultado.txt', 'w') as arquivo:
        for linha in qtable:
            linha_formatada = ' '.join([str(round(valor, 6)) for valor in linha])
            arquivo.write(linha_formatada + '\n')

# Função para pegar o index de um estado na Qtable
def pegar_index(estado):
    # Agora vamos pegar a linha do estado que estavamos e do estado que chegamos, para cada uma delas vamos extrair a plataforma a partir dos primeiros valores e converter de binario para decimal, e depois vamos calcular o index com base na plataforma e na direção que o boneco ta olhando
    #print('='*30)
    plataforma = int(estado[2:7], 2) 
    #print(f'plataforma calculada: {plataforma+1}')
    index = plataforma * 4 
    #print(f'index maximo: {index}')
    #print(f'direção dada: {int(estado[6:])}')
    index += int(estado[7:], 2) 
    #print(f'Index final: {index}')
    return index
    

# Função que faz o calculo da estimativa da recompensa
def q_func(valor_antigo, recompensa, q_maximo):
    valor_antigo += alpha * (recompensa + (gamma*q_maximo) - valor_antigo)
    return valor_antigo

# Algoritmo em si para calcular a Qtable
for c in range(eps): # Vai aplicar o algoritmo para o numero de eps
    print(f'Ep: {c+1}')
    inicio = cnt.connect(2037) # Conecta e pega o estadio inicial
    acao = random.choice(['left', 'right', 'jump'])
    estado, recompensa = cnt.get_state_reward(inicio, 'jump')

    while recompensa != -100: # Enquanto o boneco ainda tiver vivo 
        if random.uniform(0,1) < epsilon:
            acao = random.choice(['left', 'right', 'jump']) # Escolhe uma ação aleatoria para conseguir explorar
        else: # Escolhe a melhor ação
            qtable = ler_qtable_de_arquivo()
            index_antigo = pegar_index(estado)
            if max(qtable[index_antigo][0], qtable[index_antigo][1], qtable[index_antigo][2]) == qtable[index_antigo][0]:
                acao = 'left'
            elif max(qtable[index_antigo][0], qtable[index_antigo][1], qtable[index_antigo][2]) == qtable[index_antigo][1]:
                acao = 'right'
            else:
                acao = 'jump'
            print(f'Estou no Estado: {estado}, Poderia escolher entre os valores{qtable[index_antigo][0]}, {qtable[index_antigo][1]}, {qtable[index_antigo][2]}, escolhi a ação {acao}')
        print(f'Ação escolhida: {acao}')
        estado_pos_acao, recompensa = cnt.get_state_reward(inicio, acao)
        print(f' estado anterior: {estado} estado pos: {estado_pos_acao}, plataforma: {estado_pos_acao[2:7]}, direção: {estado_pos_acao[7:]}, recompensa: {recompensa}, tipo de estado é: {type(estado_pos_acao)}')
        
        # Vamos pegar os index do estado antes e pos acao
        index_antigo = pegar_index(estado)
        index_pos_acao = pegar_index(estado_pos_acao)
        print(f'index antigo: {index_antigo}, index pos acção: {index_pos_acao}')
        # Vamos abrir a Qtable para conseguir altera-la
        qtable = ler_qtable_de_arquivo()

        # Agora vamos pegar o maior valor Q que podemos acessar no novo estado que encontramos
        for i, linha in enumerate(qtable): 
            if i == index_pos_acao: 
                q_maximo = max(linha[0], linha[1], linha[2])
                break
        
        # Agora vamos atualizar o valor da ação que ele tomou com o maior valor q
        for i, linha in enumerate(qtable):
            if i == index_antigo: # Queremos a linha da qtable referente ao estado anterior para podermos altera-lo com as informações conseguidas anteriormente
                if acao == 'left':
                    linha[0] = q_func(linha[0], recompensa, q_maximo)
                elif acao == 'right':
                    linha[1] = q_func(linha[1], recompensa, q_maximo)
                else:
                    linha[2] = q_func(linha[2], recompensa, q_maximo)

        salvar_qtable(qtable)
        estado = estado_pos_acao # Para calcularmos a partir do estado que foi calculado anteriormente
        #time.sleep(30)
    


