import io
import csv
import json
from ..services.pier import Pier
import time
from concurrent import futures

ID_ESTABALECIMENTO = 0
ID_OPERACAO = 1
ID_PRODUTO = 2
MCC = 3
FLAG_OPERACAO = 4

def handle_request(row, pier):
    
    flag = row[FLAG_OPERACAO]
    estabelecimento = row[ID_ESTABALECIMENTO]
    data = {'idProduto': row[ID_PRODUTO], 'idOperacao': row[ID_OPERACAO], 'codigoMCC': row[MCC]}
    if flag == '1':
        url_habilitar = f"/estabelecimentos/{estabelecimento}/habilitar-operacao"
        res = pier.post(url_habilitar, body=json.dumps(data), format_json=True)
        if res:
            return "Habilitado com sucesso"
        else:
            return "Algo de errado"
    if flag == '0':
        url_desabilitar = f"/estabelecimentos/{estabelecimento}/desabilitar-operacao"
        res = pier.post(url_desabilitar, body=json.dumps(data), format_json=True)
        if res:
            return "Habilitado com sucesso"
        else:
            return "Algo de errado"


def all_requests(rows, count=100):
    MAX_WORKERS = 100
    workers = min(MAX_WORKERS, count)
    pier = Pier()
    with futures.ThreadPoolExecutor(workers) as executor:
        futures_list = []
        for row in rows:
            futures_list.append(executor.submit(handle_request, row, pier)) 
        for i, future_item in enumerate(futures.as_completed(futures_list)):
            pass

def handle_uploaded_csv(file):
    csv_file = file.read().decode('UTF-8')
    io_string = io.StringIO(csv_file)

    next(io_string) #pular header csv
    count = 0
    rows_ = list()
    t0 = time.time()
    csv_reader = csv.reader(io_string, delimiter=';')
    for row in csv_reader:
        rows_.append(row) 
        if count >= 1000:
            break
        count += 1
    all_requests(rows=rows_, count=count)
    print(time.time() - t0)
        

        
