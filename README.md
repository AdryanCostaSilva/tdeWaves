# TDE 2 - Algoritmo Eco

Implementação do algoritmo Eco com RabbitMQ, conforme a formalização do Item 2.

## Requisitos

- Python 3
- Biblioteca `pika` (`pip install pika`)
- RabbitMQ em execução em `localhost` (porta 5672)

## Como executar

Cada entidade roda em um terminal separado, informando seu ID e seus vizinhos:

```bash
python3 componente.py <id> [<vizinho1> <vizinho2> ...]
```

Inicie **todos** os componentes antes do starter, para que suas filas já existam. Depois, dispare o algoritmo a partir de um dos componentes:

```bash
python3 starter.py <mensagem> <destino>
```

O componente indicado em `<destino>` assume o papel de iniciador.

## Exemplo

Topologia:

```text
A: B C
B: A D E
C: A F
D: B
E: B
F: C
```

Em terminais separados:

```bash
python3 componente.py A B C
python3 componente.py B A D E
python3 componente.py C A F
python3 componente.py D B
python3 componente.py E B
python3 componente.py F C
```

Depois:

```bash
python3 starter.py GO A
```

Saída esperada no iniciador (a ordem dos IDs pode variar):

```text
iniciador: GO
ECO recebida de C
ECO recebida de B
A: lista de IDs = ['A', 'C', 'F', 'B', 'E', 'D']
A: estado = OK
```

Quando todas as entidades respondem, cada componente atinge o estado `OK` e encerra.
