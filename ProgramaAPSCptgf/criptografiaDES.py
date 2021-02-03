#Criptografia DES

import permutacao #Módulo importado para dar suporte às funções que realizam as substituiçõs e
#permutações dos blocos de bits.


#Constantes:

LARGURA = 80 #Define o valor tido como parâmetro de largura para a tela do usuário.

DIGITOS_HEXADECIMAIS = '0123456789ABCDEF' #Define os dígitos hexadecimais aceitos pelo programa.


#Funções de interação com o usuário:

def main():
    print()
    print('*' * LARGURA)
    print('CRIPTOGRAFIA DES'.center(LARGURA))
    print()
    print('Modo ECB(Eletronic CodeBook)'.center(LARGURA))
    print('*' * LARGURA)
    print()

    while True:
        #Looping infinito que encerra quando o usuário escolher sair.

        print('Digite uma opção:')
        print('\t1 - Criptografar')
        print('\t2 - Descriptografar')
        print('\t3 - Sair')

        opcao = input('Opção: ') #A escolha determina se o programa faz uma operação ou se ele é
        #encerrado.

        if opcao == '1':
            imprimirLinha('-')
            modoImpressaoChave = 'encriptar'
            operacao = 'criptografar'

        elif opcao == '2':
            imprimirLinha('-')
            modoImpressaoChave = 'decriptar'
            operacao = 'descriptografar'

        elif opcao == '3':
            imprimirLinha('-')
            print('Programa encerrado.')
            print()
            break

        else:
            #Se o usuário não digitar nenhuma das três opções é exibida uma mensagem de erro e o
            #looping volta ao início.
            print()
            print(' Opção inválida, tente novamente. '.center(LARGURA, '-'))
            print()
            continue

        mensagemBits, chaveHexa = inputUsuario(modoImpressaoChave)

        outputUsuario(mensagemBits, chaveHexa, operacao)

def imprimirLinha(simbolo):
    #imprime, entre duas linhas em branco, uma linha composta pelo caractere passado como argumento.

    print()
    print(simbolo * LARGURA)
    print()

def inputUsuario(modo):
    #Pede ao usuário digitar o valor da chave e da mensagem e manipula esses valores.

    while True:
        #Looping infinito que é encerrado quando o usuário digita uma chave hexadecimal com 16 ou menos dígitos.

        chaveDigitada = input('Chave de %sção hexadecimal: ' %(modo[:-1])) #A variável modo define qual é o tipo de
        #chave hexadecimal que o usuário deve digitar.

        if identificarInput(chaveDigitada) != 'hexadecimal':
            #Se a chave não for hexadecimal, exibe uma mensagem de erro e retorna ao início do looping para que o
            #usuario digite novamente.

            print()
            print(' A chave digitada não possui dígitos hexadecimais válidos, tente novamente. '.center(LARGURA, '.'))
            print((' Dígitos hexadecimais: %s ' %(DIGITOS_HEXADECIMAIS)).center(LARGURA, '.'))
            print()
            continue

        if len(chaveDigitada) > 16:
            #Exibe uma mensagem de erro caso a chave seja muito grande e retorna ao início do looping.

            print()
            print(' A chave não pode ter mais que 16 dígitos. '.center(LARGURA, '.'))
            print()
            continue

        if len(chaveDigitada) < 16:
            #Se necessário, adiciona zeros à esquerda do valor da chave digitada pelo usuário para que ela tenha
            #exatamente 16 dígitos, depois sai do looping.

            chaveDigitada = '0' * (16 - len(chaveDigitada)) + chaveDigitada

        break

    mensagemDigitada = input('\nDigite uma mensagem: ')

    tipoInputMensagem = identificarInput(mensagemDigitada) #A função chamada retorna o provável tipo de
    #mensagem que o usuário digitou(texto ou hexadecimal) e essa string é armazenada na variável.

    if tipoInputMensagem == 'texto':
        mensagemBits = stringBits(mensagemDigitada) #converte a mensagem de string para vetor de bits.

    if tipoInputMensagem == 'hexadecimal':
        mensagemBits = hexaBits(mensagemDigitada) #converte a mensagem de hexadecimal para vetor de bits.

    return mensagemBits, chaveDigitada

def identificarInput(valor):
    #Esta função tenta classificar qual é o tipo de valor passado a ela dentre os dois possíveis,
    #string de texto ou string hexadecimal, verificando se os caracteres do valor estão ou não estão
    #dentre os caracteres considerados dígitos hexadecimais.


    for caractere in valor:
            if caractere not in DIGITOS_HEXADECIMAIS:

                return 'texto'

    return 'hexadecimal'

def outputUsuario(mensagemBits, chaveHexa, operacao):
    #Exibe o valor da chave e da mensagem, faz a encriptação/decriptação e mostra os resultados.

    imprimirLinha('-')
    print('Chave: %s' %(chaveHexa))
    print('\nMensagem(texto):\n"%s"' %(bitsString(mensagemBits))) #Exibe a mensagem convertida para
    #texto.

    print('\nMensagem(hexadecimal):\n%s' %(bitsHexa(mensagemBits))) #Exibe a mensagem convertida para
    #hexadecimal.

    print('\n%sndo...' %(operacao[:-1]).title()) #Exibe a operação a ser realizada.

    mensagemTraduzidaBits = traduzir(mensagemBits, hexaBits(chaveHexa), operacao) #Envia os bits da
    #mensagem, da chave e a operação correspondente para a função que retorna os bits da nova mensagem.

    print('\nMensagem %sda(texto):\n"%s"' %(operacao[:-1], bitsString(mensagemTraduzidaBits))) #Exibe
    #a tradução correspondente convertida em texto.

    print('\nMensagem %sda(hexadecimal):\n%s' %(operacao[:-1], bitsHexa(mensagemTraduzidaBits))) #Exibe
    #a tradução correspondente convertida em hexadecimal.

    imprimirLinha('-')


#Funções de criptografia/descriptografia:

def traduzir(mensagemBits, chaveBits, operacao):
    #Com os vetores de bits da mensagem e da chave, realiza todas as etapas da respectiva operação
    #e retorna o vetor de bits da nova mensagem.
    #A simetria entre a encriptação e a decriptação permite que apenas um trecho do código seja
    #efetivamente diferente para cada operação.

    traducaoBits = [] #Vetor sem bits.

    for i in range(0, len(mensagemBits), 64):
        #Iteração para separar a mensagem em blocos.

        bloco64bits = mensagemBits[i : i + 64] #Selecionando um bloco de 64 bits.

        #Passo 1: Permutação inicial

        bloco64bits = permutacaoInicial(bloco64bits) #A permutação inicial é equivalente à
        #permutação final inversa.

        #Passo 2: Cisão em blocos de 32 bits e 16 iterações

        if operacao == 'criptografar':
            L = bloco64bits[:32] #Os primeiros 32 bits formam o bloco L.
            R = bloco64bits[32:] #Os últimos 32 bits formam o bloco R.

            for n in range(1, 17):
                L_n = R #O bloco L da rodada recebe o valor do bloco R anterior.

                R_n = portaXOR(funcao_f(R, chaveBits, n), L) #O bloco R da rodada recebe o valor da
                #operação XOR entre os bits da função f, que usa o bloco R anterior e a sub-chave da
                #rodada, e os bits do bloco L anterior.

                L = L_n #Armazenando o valor de L que será utilizado na próxima rodada.
                R = R_n #Armazenando o valor de R que será utilizado na próxima rodada.

            bloco64bits = R_n + L_n #O L e o R da rodada 16 formam um bloco de 64 bits, com o R
            #formando os primeiros bits e o L os últimos.

        if operacao == 'descriptografar':
            R_n = bloco64bits[:32] #os primeiros 32 bits formam o bloco R da rodada 16.
            L_n = bloco64bits[32:] #os últimos 32 bits formam o bloco L da rodada 16.

            for n in range(16, 0, -1):
                R = L_n #O bloco R da rodada anterior recebe o valor do bloco L da rodada.

                L = portaXOR(funcao_f(L_n, chaveBits, n), R_n) #O bloco L da rodada anterior recebe
                #o valor da operação XOR entre os bits da função f, que usa o bloco L da rodada e a
                #sub-chave da rodada, e os bits do bloco R da rodada.

                R_n = R #armazenando o valor do R que será utilizado na próxima rodada.
                L_n = L #armazenando o valor do L que será utilizado na próxima rodada.

            bloco64bits = L + R #Reunindo os valores do primeiro R e do primeiro L formados na
            #criptografia para obter o bloco da primeira permutação.

        #Passo 3: Permutação final

        bloco64bits = permutacaoFinal(bloco64bits) #A permutação final é equivalente à permutação
        #inicial inversa.

        traducaoBits.extend(bloco64bits) #Adiciona ao vetor criado anteriormente os bits do bloco
        #de 64 bits permutado.

    return traducaoBits #Vetor com todos os bits da mensagem traduzida.

def gerarSubChave(chave64bits, rodada):
    #Recebe o vetor de bits da chave e o número da rodada, retorna a sub-chave da rodada.

    #Passo 1: Permutação PC - 1

    chave56bits = permutacaoPC1(chave64bits)

    #Passo 2: Cisão em blocos de 28 bits e rotação à esquerda

    C = chave56bits[:28] #Os 28 primeiros bits formam o bloco C.
    D = chave56bits[28:] #Os 28 últimos bits formam o bloco D.

    #Neste programa os blocos C e D da rodada são diretamente gerados rotacionando os blocos C e D
    #iniciais.

    rotacionarEsquerda(C, rodada) #Rotacionando o bloco C.
    rotacionarEsquerda(D, rodada) #Rotacionando o bloco D.

    #Passo 3: Permutação PC - 2

    subChave_rodada = permutacaoPC2(C + D) #Os blocos C e D rotacionados são agrupados num único
    #bloco que será permutado.

    return subChave_rodada

def permutacaoPC1(chave64bits):
    #Permutação que remove os bits de paridade da chave e resulta em um bloco de 56 bits.

    chave56bits = [] #Vetor sem bits.

    for i in permutacao.PC1:
        #O looping itera sobre cada número dentro do vetor PC1(variável do módulo permutacao).

        chave56bits.append(chave64bits[i]) #O bit do vetor chave64bits no índice i é adicionado ao
        #vetor chave56bits.

    #O vetor chave56bits contém os bits permutados da chave, note que os bits de paridade foram
    #ignorados.

    return chave56bits

def permutacaoPC2(chave56bits):
    #Permutação que produz as sub-chaves de 48 bits.

    chave48bits = [] #Vetor sem bits.

    for i in permutacao.PC2:
        #O looping itera sobre cada número dentro do vetor PC2(variável do módulo permutacao).

        chave48bits.append(chave56bits[i]) #O bit do vetor chave56bits no índice i é adicionado ao
        #vetor chave48bits.

    #A partir de um vetor de 56 bits se obtém uma sub-chave de 48 bits.

    return chave48bits

def permutacaoInicial(bloco64bits):

    bloco64bitsPermutado = [] #Vetor sem bits.

    for i in permutacao.IP:
        #O looping itera sobre cada número dentro do vetor IP(variável do módulo permutacao).

        bloco64bitsPermutado.append(bloco64bits[i]) #O bit do vetor bloco64bits no índice i é
        #adicionado ao vetor bloco64bitsPermutado.

    return bloco64bitsPermutado

def funcao_f(bloco32bits, chave, rodada):
    #Opera com um bloco de 32 bits e uma sub-chave de 48 bits, produzindo um bloco de 32 bits.

    subChave = gerarSubChave(chave, rodada) #Gera a sub-chave da rodada.

    #Passo 1: Expansão E

    E = funcaoExpansao(bloco32bits) #Produz um bloco de 48 bits.

    #Passo 2: XOR com a sub-chave da rodada

    xor = portaXOR(E, subChave) #XOR com dois blocos de 48 bits.

    #Passo 3: Substituição usando caixas-S

    bloco32bits = substituicaoCaixas_S(xor)

    #Passo 4: Permutação

    f = permutar(bloco32bits)

    return f

def funcaoExpansao(bloco32bits):
    #Expande um bloco de 32 bits para 48 bits.

    bloco48bits = [] #Vetor sem bits.

    for i in permutacao.E:
        #O looping itera sobre cada número dentro do vetor E(variável do módulo permutacao).

        bloco48bits.append(bloco32bits[i]) #O bit do vetor bloco32bits no índice i é adicionado ao
        #vetor bloco48bits.

    #Note que para aumentar o tamanho do bloco de 32 bits, alguns bits são repetidos durante a
    #permutação.

    return bloco48bits

def substituicaoCaixas_S(bloco48bits):
    #Separa um bloco de 48 bits em oito blocos de 6 bits que são transformados em oito blocos de 4
    #bits e depois os reune para formar um bloco de 32 bits.
    #As caixas-S são tabelas com linhas e colunas, neste programa elas estão armazenadas no vetor
    #S_BOX(variável do módulo permutacao) que contém 8 matrizes que representam as tabelas.

    bloco32bits = [] #Vetor sem bits.

    for caixa_S in range(8):
        #Iteração para separar os oito blocos de 6 bits e as oito caixas-S.

        bloco6bits = bloco48bits[caixa_S * 6 : (caixa_S + 1) * 6] #O número Caixa_S é utilizado para
        #criar o intervalo de 6 bits.

        linha = int(bloco6bits[0] + bloco6bits[5], 2) #O primeiro e o último bit do bloco formam um
        #número decimal que define a linha.

        coluna = int(''.join(bloco6bits[1:5]), 2) #Os quatro bits centrais formam um número decimal
        #que define a coluna.

        bloco4bits = (bin(permutacao.S_BOX[caixa_S][linha][coluna]))[2:] #O número Caixa_S indica
        #qual matriz será usada, o número decimal dessa matriz que estiver na linha e coluna
        #indicadas é convertido para binário. Essa conversão resulta em uma string com os dois
        #primeiros caracteres indicando que se trata de um número binário, esses caracteres não são
        #necessários para o programa e por isso são cortados.

        bloco4bits = '0' * (4 - len(bloco4bits)) + bloco4bits #Se a string tiver menos que 4 dígitos
        #binários, adiciona-se zeros à esquerda para que ela tenha exatamente 4 dígitos.

        bloco32bits.extend(list(bloco4bits)) #Transforma a string em um vetor de bits e adiciona
        #cada bit ao vetor bloco32bits.

    return bloco32bits

def permutar(bloco32bits):

    bloco32bitsPermutado = [] #Vetor sem bits.

    for i in permutacao.P:
        #O looping itera sobre cada número dentro do vetor P(variável do módulo permutacao).

        bloco32bitsPermutado.append(bloco32bits[i]) #O bit do vetor bloco32bits no índice i é
        #adicionado ao vetor bloco32bitsPermutado.

    return bloco32bitsPermutado

def permutacaoFinal(bloco64bits):

    bloco64bitsPermutado = [] #Vetor sem bits.

    for i in permutacao.FP:
        #O looping itera sobre cada número dentro do vetor FP(variável do módulo permutacao).

        bloco64bitsPermutado.append(bloco64bits[i]) #O bit do vetor bloco64bits no índice i é
        #adicionado ao vetor bloco64bitsPermutado.

    return bloco64bitsPermutado

#Funções auxiliares do processo de criptografia/descriptografia:

def rotacionarEsquerda(chave28bits, rodada):
    #Executa o processo de rotação usado na geração de sub-chaves.

    rotacoes = permutacao.ROTACOES[rodada] #Dentro do dicionário do módulo permutacao, o valor
    #atribuído à chave de número correspondente ao número da rodada é armazenado. Esse valor é o
    #número de rotações a serem realizadas.

    for i in range(rotacoes):
        bitRemovido = chave28bits.pop(0) #remove o primeiro bit do vetor.
        chave28bits.append(bitRemovido) #adiciona o bit removido ao vetor.

        #Note que ao retirar o primeiro bit, todos os outros bits se deslocam para a esquerda de
        #sua posição original.

    #Esta função não necessita de retorno porque ela faz uma cópia da referência da lista passada
    #como argumento, ou seja, todas as alterações feitas com a referência da lista consequentemente
    #alteram a lista em si.

def portaXOR(A, B):
    #Porta lógica XOR bit a bit com dois vetores de bits de mesmo tamanho.

    saida = []

    for bit in range(len(A)):
        #O looping itera sobre o tamanho de um dos vetores.
        #A operação lógica é feita entre os bits com o mesmo índice.

        if A[bit] != B[bit]:
            saida.append('1') #Se os bits forem diferentes a saída é 1.

        else:
            saida.append('0') #Se os bits forem iguais a saída é 0.

    return saida


#Funções de conversão:

def hexaBits(hexadecimal):
    #Recebe uma string hexadecimal, cada dois dígitos hexadecimais são convertidos para o byte
    #correspondente e retorna um vetor de bits com tamanho divisivel por 64.

    vetorBits = [] #Vetor sem bits.

    for i in range(0, len(hexadecimal), 2):
        #Iteração que ajuda a separar os dígitos hexadecimais em grupos de 2 dígitos.

        numeroHex = hexadecimal[i : i + 2] #Seleciona dois dígitos da string.

        byte = bin(int(numeroHex, 16))[2:] #Converte o número hexadecimal para decimal e depois para
        #binário. Essa conversão resulta em uma string com os dois primeiros caracteres indicando
        #que se trata de um número binário, esses caracteres não são necessários para o programa e
        #por isso são cortados.

        byte = '0' * (8 - len(byte)) + byte #Se a string tiver menos que 8 dígitos binários,
        #adiciona-se zeros à esquerda para que ela tenha exatamente 8 dígitos.

        vetorBits.extend(list(byte)) #Transforma a string em um vetor de bits e adiciona cada bit ao
        #vetor vetorBits.

    resto = len(vetorBits) % 64 #Armazena o resto da divisão do tamanho do vetor de bits por 64.

    if resto:
        #Se o resto não for 0, adiciona-se zeros ao vetor para que seu tamanho seja divisível por 64.

        vetorBits.extend(['0'] * (64 - resto))

    return vetorBits

def bitsHexa(vetorBits):
    #Converte um vetor de bits para uma string de dígitos hexadecimais.

    hexadecimal = []

    for i in range(0, len(vetorBits), 8):
        #Iteração que ajuda a separar os bits em grupos de bytes.

        byte = ''.join(vetorBits[i : i + 8]) #Seleciona oito bits do vetor e forma uma string.

        numeroHex = hex(int(byte, 2))[2:] #Converte os bits para um número decimal e depois para
        #hexadecimal. Essa conversão resulta em uma string com os dois primeiros caracteres
        #indicando que se trata de um número hexadecimal, esses caracteres não são necessários para
        #o programa e por isso são cortados.

        numeroHex = '0' * (2 - len(numeroHex)) + numeroHex #Se a string tiver apenas 1 dígito
        #hexadecimal, adiciona-se um zero à esquerda para que ela tenha exatamente 2 dígitos.

        hexadecimal.append(numeroHex)

    return ''.join(hexadecimal).upper() #Retorna as strings do vetor hexadecimal concatenadas e em
    #maiúsculo.

def stringBits(string):
    #Converte uma string de caracteres para um vetor de bits.

    hexadecimal = []

    for char in string:
        #Itera sobre todos os caracteres.

        numeroHex = hex(ord(char))[2:] #O caractere é convertido para um número decimal da tabela
        #ASCII e depois para hexadecimal. Essa conversão resulta em uma string com os dois primeiros
        #caracteres indicando que se trata de um número hexadecimal, esses caracteres não são
        #necessários para o programa e por isso são cortados.

        numeroHex = '0' * (2 - len(numeroHex)) + numeroHex #Se a string tiver apenas 1 dígito
        #hexadecimal, adiciona-se um zero à esquerda para que ela tenha exatamente 2 dígitos.

        hexadecimal.append(numeroHex)

    vetorBits = hexaBits(''.join(hexadecimal)) #Concatena as strings do vetor hexadecimal e
    #converte para bits.

    return vetorBits

def bitsString(vetorBits):
    #Converte um vetor de bits para uma string de caracteres.

    string = []

    hexadecimal = bitsHexa(vetorBits) #Converte o vetor para hexadecimal.

    for i in range(0, len(hexadecimal), 2):
        #Iteração que ajuda a separar os dígitos hexadecimais em grupos de 2 dígitos.

        numeroHex = hexadecimal[i : i + 2] #Seleciona dois dígitos da string.

        char = chr(int(numeroHex, 16)) #O número hexadecimal é convertido para decimal e depois para
        #um caractere da tabela ASCII.

        string.append(char)

    return ''.join(string) #Retorna os caracteres do vetor concatenados.

if __name__ == '__main__':
    main()
