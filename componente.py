#!/usr/bin/env python3

# Componente Básico
# EP - PUCPR
# Prof. Luiz Lima Jr.

from pika import BlockingConnection
from sys import argv
from enum import Enum

if len(argv) < 2:
    print(f"USO: {argv[0]} <id> [<v1> <v2> ...]")
    exit(1)

Estado = Enum('Estado', ['OCIOSO', 'INICIADOR', 'ATIVO', 'OK'])

idx = argv[1]
Nx = argv[2:]
estado = Estado.OCIOSO       # estado inicial
entrada = None               # vizinho que me enviou EXPLORAR
aguardando = set()           # vizinhos dos quais ainda aguardo ECO
info = []                    # informacoes (IDs) recebidas dos vizinhos

print("meu id =", idx)
print("meus vizinhos =", Nx)

conexao = BlockingConnection()
canal = conexao.channel()

canal.queue_declare(queue=idx, durable=True, auto_delete=True)

# envia mensagem para dest
def envia(msg, dests):
    for dest in dests:
        canal.basic_publish(exchange="",
                            routing_key=dest,
                            body=f"{idx}:{msg}")

def finaliza():
    global estado
    estado = Estado.OK
    print(f"{idx}: estado = OK", flush=True)
    canal.stop_consuming()

def junta_ids(dados_recebidos):
    # ID da entidade concatenado com as informacoes recebidas dos vizinhos
    ids = [idx]
    for dados in dados_recebidos:
        if dados:
            ids.extend(dados.split(","))
    return ids

def recebendo(msg, origem, dados):
    global estado, entrada, aguardando, info

    if msg == "EXPLORAR":
        # so processa a primeira EXPLORAR recebida (estado OCIOSO)
        if estado == Estado.OCIOSO:
            print(f"EXPLORAR recebida de {origem}")
            entrada = origem
            estado = Estado.ATIVO
            aguardando = set(Nx) - {origem}
            if aguardando:
                envia("EXPLORAR", aguardando)
            else:
                # nao tem vizinhos alem da origem
                envia(f"ECO:{idx}", [origem])
                finaliza()
        else:
            # ja participei: responde ECO imediatamente (grafos com ciclos)
            envia("ECO", [origem])
    elif msg == "ECO":
        if estado in (Estado.INICIADOR, Estado.ATIVO) and origem in aguardando:
            print(f"ECO recebida de {origem}")
            info.append(dados)
            aguardando.discard(origem)
            if not aguardando:
                ids = junta_ids(info)
                if estado == Estado.INICIADOR:
                    # todas as entidades responderam
                    print(f"{idx}: lista de IDs = {ids}", flush=True)
                else:
                    envia(f"ECO:{','.join(ids)}", [entrada])
                finaliza()

def espontaneamente(msg):
    global estado, aguardando
    estado = Estado.INICIADOR
    print("iniciador:", msg)
    aguardando = set(Nx)
    if aguardando:
        envia("EXPLORAR", aguardando)
    else:
        print(f"{idx}: lista de IDs = {[idx]}", flush=True)
        finaliza()

def callback(canal, metodo,  props, corpo):
    partes = corpo.decode().split(":", 2)
    if len(partes) < 2:
        # nao tem origem
        msg = partes[0]
        origem = "STARTER"
        dados = ""
    else:
        origem = partes[0]
        msg = partes[1]
        dados = partes[2] if len(partes) > 2 else ""

    if origem.upper()=="STARTER":
        espontaneamente(msg)
    else:
        recebendo(msg, origem, dados)

canal.basic_consume(queue=idx,
                    on_message_callback=callback,
                    auto_ack=True)

try:
    print(f"{idx}: aguardando mensagens...")
    canal.start_consuming()
except KeyboardInterrupt:
    canal.stop_consuming()

conexao.close()
print("Terminando")
