import os
from modules.order import Order
import pandas as pd

valid_orders = []
invalid_orders = []

def import_orders(df):
    for index, row in df.iterrows():
        try:
            new_invoice = Order(index=index + 2, name=row['Nome'], email=row['E-mail'], product=row['Produto'], qunatity=row['Quantidade'], unit_value=row['Valor Unitário'])
            valid_orders.append(new_invoice)
        except ValueError as e:
            new_invoice = dict()
            new_invoice['index'] = index + 2
            new_invoice['name'] = row['Nome']
            new_invoice['email'] = row['E-mail']
            new_invoice['product'] = row['Produto']
            new_invoice['qunatity'] = row['Quantidade']
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
    try:
        df = pd.read_excel('./files/orders.xlsx')
        import_orders(df)
    except Exception as e:
        os.system('cls')
        print(f'Houve um erro ao importar a planilha de pedidos.\nDescrição do erro:\n{e}')
    
    
if __name__ == '__main__':
    main()