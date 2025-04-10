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
            new_invoice = Order(index=index + 2, name=row['Nome'], email=row['E-mail'], product=row['Produto'], quantity=row['Quantidade'], unit_value=row['Valor Unitário'])
            valid_orders.append(new_invoice)
        except ValueError as e:
            new_invoice = dict()
            new_invoice['index'] = index + 2
            new_invoice['name'] = row['Nome']
            new_invoice['email'] = row['E-mail']
            new_invoice['product'] = row['Produto']
            new_invoice['quantity'] = row['Quantidade']
            new_invoice['unitValue'] = row['Valor Unitário']
            invalid_orders.append(new_invoice)

    os.system('cls')
    msg = f'''************************************************************************************************************************
- Total de pedidos importados: {len(valid_orders)}
'''
    print(msg)
    
    if invalid_orders:
        error_message = '''************************************************************************************************************************
Os pedidos das linhas apresentadas abaixo contém inconsistências, por gentileza, verifique-os:\n'''
        for invoice in invalid_orders:
            error_message += f' - Linha {invoice['index']}\n'
        
        print(f'- Total de pedidos com erro: {len(invalid_orders)}\n')
        print(error_message)

def main():
    url = URL + SEND_ORDER_ROUTE
    
    try:
        df = pd.read_excel('./files/orders.xlsx')
        import_orders(df)
    except Exception as e:
        os.system('cls')
        print(f'Houve um erro ao importar a planilha de pedidos.\nDescrição do erro:\n{e}')

    for current_order in valid_orders:
        print(current_order.index)
        order = {
            'index': current_order.index,
            'name': current_order.name,
            'email': current_order.email,
            'product': current_order.product,
            'quantity': current_order.quantity,
            'unit_value': current_order.unit_value
        }

        response = requests.post(url, json=order)

        if response.status_code == 200:
            print(f'Pedido {current_order.index} enviado com sucesso!\n\n')
        else:
            print(f'Houve uma falha ao enviar o pedido {current_order.index}\nCódigo do erro: {response.status_code}\n')
        
        sleep(2)
    
if __name__ == '__main__':
    main()