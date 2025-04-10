from modules.order import Order
from time import sleep
import os
import logging
import pandas as pd
import requests

logging.basicConfig(filename='orders.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

URL = 'http://127.0.0.1:8000'
SEND_ORDER_ROUTE='/api/orders'

valid_orders = []
invalid_orders = []

def import_orders(df):
    for index, row in df.iterrows():
        try:
            logging.info('-----------------------------------')
            logging.info(f'Importando pedido {index + 2}...')
            new_invoice = Order(index=index + 2, name=row['Nome'], email=row['E-mail'], product=row['Produto'], quantity=row['Quantidade'], unit_value=row['Valor Unitário'])
            valid_orders.append(new_invoice)
            logging.info('Pedido importado com sucesso')
        except ValueError as e:
            new_invoice = dict()
            new_invoice['index'] = index + 2
            new_invoice['name'] = row['Nome']
            new_invoice['email'] = row['E-mail']
            new_invoice['product'] = row['Produto']
            new_invoice['quantity'] = row['Quantidade']
            new_invoice['unitValue'] = row['Valor Unitário']
            logging.info('Houve um erro ao importar o pedido.')
            logging.info(f'Dados do pedido: {new_invoice}')
            invalid_orders.append(new_invoice)

    logging.info('==============================================')
    logging.info(f'- Total de pedidos importados: {len(valid_orders)}')
    
    if invalid_orders:
        logging.info(f'- Total de pedidos com erro: {len(invalid_orders)}')
    
    logging.info('==============================================')

def main():
    url = URL + SEND_ORDER_ROUTE

    logging.info('*********************************************************')
    logging.info('Iniciando processo de importacao de tabela de pedidos')

    try:
        df = pd.read_excel('./files/orders.xlsx')
        import_orders(df)
    except Exception as e:
        logging.info(f'Houve um erro ao importar a planilha de pedidos.\nDescricao do erro:{e}\n')

    for current_order in valid_orders:
        logging.info('*********************************************************')
        logging.info('Iniciando envio de pedidos')
        
        order = {
            'index': current_order.index,
            'name': current_order.name,
            'email': current_order.email,
            'product': current_order.product,
            'quantity': current_order.quantity,
            'unit_value': current_order.unit_value
        }

        logging.info('---------------------------------------')
        logging.info(f'Enviando pedido {order['index']}\n')
        logging.info(f'Dados do pedido: {order}\n')

        response = requests.post(url, json=order)

        if response.status_code == 200:
            logging.info(f'Pedido enviado com sucesso!\n')
        else:
            logging.info(f'Houve uma falha ao enviar o pedido {current_order.index}\nCódigo do erro: {response.status_code}\n')
        
        sleep(2)
    
    logging.info('Fim do processo de importacao.')
    logging.info('*********************************************************')
    
if __name__ == '__main__':
    main()