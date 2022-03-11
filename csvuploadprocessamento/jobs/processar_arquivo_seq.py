import io
import csv
import json
from ..services.pier import Pier
import time

from celery import shared_task


@shared_task(bind=True)
def handle_uploaded_csv(self, file):

    pier = Pier()
    ID_ESTABALECIMENTO = 0
    ID_OPERACAO = 1
    ID_PRODUTO = 2
    MCC = 3
    FLAG_OPERACAO = 4

    csv_file = file.read().decode('UTF-8')
    io_string = io.StringIO(csv_file)

    next(io_string) #pular header csv
    t0 = time.time()
    count = 0
    for row in csv.reader(io_string, delimiter=';'):
        flag = row[FLAG_OPERACAO]
        estabelecimento = row[ID_ESTABALECIMENTO]
        data = {'idProduto': row[ID_PRODUTO], 'idOperacao': row[ID_OPERACAO], 'codigoMCC': row[MCC]}
        
        if flag == '1':
            url_habilitar = f"/estabelecimentos/{estabelecimento}/habilitar-operacao"
            pier.post(url_habilitar, body=json.dumps(data), format_json=True)
        if flag == '0':
            url_desabilitar = f"/estabelecimentos/{estabelecimento}/desabilitar-operacao"
            pier.post(url_desabilitar, body=json.dumps(data), format_json=True)
        if count >= 10:
            print(f"Tempo finalizado: {time.time() - t0}")
            break
        count += 1
        self.update_state(
            state="PROGRESS",
            meta={'current': count}
        )
        
