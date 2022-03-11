import io, csv, time, asyncio
from ..services.pier_async import Pier
from aiohttp.client_exceptions import ClientResponseError
from celery import shared_task
from celery_progress.backend import ProgressRecorder

async def handle_request(row, pier, semaphore):
    async with semaphore:

        ID_ESTABALECIMENTO = 0
        ID_OPERACAO = 1
        ID_PRODUTO = 2
        MCC = 3
        FLAG_OPERACAO = 4

        flag = row[FLAG_OPERACAO]
        estabelecimento = row[ID_ESTABALECIMENTO]
        data = {'idProduto': row[ID_PRODUTO], 'idOperacao': row[ID_OPERACAO], 'codigoMCC': row[MCC]}

        if flag == '1':
            try:
                url_habilitar = f"/estabelecimentos/{estabelecimento}/habilitar-operacao"
                res = await pier.post(url=url_habilitar, json=data)
            except ClientResponseError as e:
                print(e)

        if flag == '0':
            try:
                url_desabilitar = f"/estabelecimentos/{estabelecimento}/desabilitar-operacao"
                res = await pier.post(url=url_desabilitar, json=data)
            except ClientResponseError as e:
                print(e)

async def all_requests(self, rows):
    pier = Pier()
    progress_recorder = ProgressRecorder(self)
    total = len(rows)
    counter = 0
    semaphore = asyncio.BoundedSemaphore(100)
    tasks = []
    for row in rows:
        tasks.append(handle_request(row=row, pier=pier, semaphore=semaphore)) 
    
    for task in asyncio.as_completed(tasks):
        res = await task
        print(res)
        counter += 1
        progress_recorder.set_progress(counter, total)

    await pier.close()


@shared_task(bind=True)
def handle_uploaded_csv(self,file):
    csv_file = file.read().decode('UTF-8')
    io_string = io.StringIO(csv_file)
    next(io_string) #pular header csv
    
    rows_ = list()

    csv_reader = csv.reader(io_string, delimiter=';')
    for row in csv_reader:
        rows_.append(row) 
    io_string.close()
    t0 = time.time()
    asyncio.run(all_requests(self, rows=rows_))
    print(time.time() - t0)
        

        
