# Notes TDE 2 Wave - Programação Distribuída

Requisição em broadcast para as outras entidades responderem com a informação solicitada -> Wave

O algoritmo só termina quando todas as entidades responderem a requisição.

# Algoritmo Eco

Restrições:
- Confiabilidade total
- Conectividade
- Links Bidirecionais
- Iniciador Único

O iniciador envia uma requisição para todos os vizinhos, a entidade recebe a requisição, e, caso seja a primeira vez que recebeu, envia para todos os seus vizinhos (com exceção do vizinho que enviou).
Quando uma entidade recebe a requisição de todos os seus vizinhos, adiciona a suas informações e envia para o vizinho que lhe enviou, e assim vai indo até chegar no iniciador.
Quando chega no iniciador, ele entende que todos receberem e enfim encerra o algoritmo.


# Item 2

Formalização do algoritmo Eco.


# Item 3

Implementar de acordo com o template usado na aula e com a formalização feita no Item 2.

A informação que a entidade adiciona deve ser o seu ID (String) concatenada com todas as informações que recebeu de seus vizinhos.
Após receber todas as informações, o iniciador deve fazer um print da lista de IDs.
Usar RabbitMQ tal como foi utilizado na aula.


# Envio

Formalização do Item 2 e o código feito no Item 3.
