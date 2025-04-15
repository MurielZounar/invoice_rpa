from modules.order import Order
from time import sleep
import os
import logging
import pandas as pd
import requests
import streamlit as st

logging.basicConfig(filename='orders.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

URL = 'http://127.0.0.1:8000'
SEND_ORDER_ROUTE='/api/orders'

st.title('OrderFlow - Validação e Envio de Pedidos (RPA)')
st.subheader('Faça upload de uma planilha Excel com pedidos, valide os dados automaticamente e envie os pedidos válidos para a API com apenas um clique.', divider='orange')
file = st.file_uploader('Selecione um arquivo:', type=['xlsx', 'xls'])

def send_orders(orders):
    logging.info('*********************************************************')
    logging.info('Iniciando envio de pedidos')
    url = URL + SEND_ORDER_ROUTE
    success = True 

    logging.info(f'SEND_ORDERS:\n{orders}')

    with st.spinner("Enviando para a API..."):
        for current_order in orders:
            order = {
                'index': current_order['index'],
                'name': current_order['name'],
                'email': current_order['email'],
                'product': current_order['product'],
                'quantity': current_order['quantity'],
                'unit_value': current_order['unitValue']
            }

            logging.info('---------------------------------------')
            logging.info(f'Enviando pedido {order['index']}\n')
            logging.info(f'Dados do pedido: {order}\n')

            response = requests.post(url, json=order)
            if response.status_code == 200:
                logging.info(f'Pedido enviado com sucesso!\n')
            else:
                logging.info(f'Houve uma falha ao enviar o pedido {current_order['index']}\nCódigo do erro: {response.status_code}\n')
                success = False
        
        if success:
            st.success("✅ Todos os pedidos foram enviados com sucesso!")
        else:
            st.warning("⚠️ Houve falhas no envio de alguns pedidos. Verifique os logs.")

        st.divider()
        if st.button("📥 Importar Nova Planilha"):
            st.session_state.pop('valid_orders', None)
            st.session_state.pop('invalid_orders', None)
            st.session_state.pop('uploaded_file', None)
            st.session_state.uploaded_file = None
            st.session_state.show_import_btn = True

def import_orders(file):
    logging.info('*********************************************************')
    logging.info('Iniciando processo de importacao de tabela de pedidos')

    valid_orders = []
    invalid_orders = []

    try:
        df = pd.read_excel(file)
        with st.spinner("importando..."):
            for index, row in df.iterrows():
                try:
                    logging.info('-----------------------------------')
                    logging.info(f'Importando pedido {index + 2}...')
                    new_order = Order(index=index + 2, name=row['Nome'], email=row['E-mail'], product=row['Produto'], quantity=row['Quantidade'], unit_value=row['Valor Unitário'])
                    order = dict()
                    order['index'] = index + 2
                    order['name'] = row['Nome']
                    order['email'] = row['E-mail']
                    order['product'] = row['Produto']
                    order['quantity'] = row['Quantidade']
                    order['unitValue'] = f'{float(row['Valor Unitário']):2f}'
                    valid_orders.append(order)
                    logging.info('Pedido importado com sucesso')
                except ValueError as e:
                    new_order = dict()
                    new_order['index'] = index + 2
                    new_order['name'] = row['Nome']
                    new_order['email'] = row['E-mail']
                    new_order['product'] = row['Produto']
                    new_order['quantity'] = row['Quantidade']
                    new_order['unitValue'] = f'{float(row['Valor Unitário']):2f}'
                    logging.info('Houve um erro ao importar o pedido.')
                    logging.info(f'Dados do pedido: {new_order}')
                    invalid_orders.append(new_order)
                # sleep(0.1)
    except Exception as e:
        logging.info(f'Houve um erro ao importar a planilha de pedidos.\nDescricao do erro:{e}\n')

    st.toast('Importação concluída', icon='✅')
    
    if st.session_state.show_dataframes:
        if valid_orders:
            st.session_state.orders = valid_orders
            st.session_state.show_send_btn = True

        st.text('Pedidos válidos:')
        st.dataframe(valid_orders,
                    column_config={
                        'index': 'ID',
                        'name': 'Nome',
                        'email': 'E-mail',
                        'product': 'Produto',
                        'quantity': 'QTD',
                        'unitValue': st.column_config.NumberColumn('Valor Unitário', format='R$ %d')
                    },
                    key='valid_df')
        st.text(f'Total de pedidos válidos: {len(valid_orders)}')

        st.divider()
        st.text('Pedidos inválidos:')
        st.dataframe(invalid_orders,
                    column_config={
                        'index': 'ID',
                        'name': 'Nome',
                        'email': 'E-mail',
                        'product': 'Produto',
                        'quantity': 'QTD',
                        'unitValue': st.column_config.NumberColumn('Valor Unitário', format='R$ %d')
                    },
                    key='invalid_df')
        st.text(f'Total de pedidos inválidos: {len(invalid_orders)}')

    logging.info('==============================================')
    logging.info(f'- Total de pedidos importados: {len(valid_orders)}')
    st.session_state.import_done = True
    
    if invalid_orders:
        logging.info(f'- Total de pedidos com erro: {len(invalid_orders)}')
    
    logging.info('==============================================')

def main():
    if file:
        st.session_state.uploaded_file = file

        if 'orders' not in st.session_state:
            st.session_state.orders = False

        if 'show_dataframes' not in st.session_state:
            st.session_state.show_dataframes = False

        if 'show_send_btn' not in st.session_state:
            st.session_state.show_send_btn = False

        if 'import_done' not in st.session_state:
            st.session_state.import_done = False
        
        if st.button('📥 Importar Pedidos', key='import_orders'):
            st.session_state.show_import_btn = False
            st.session_state.show_dataframes = True
            if not st.session_state.import_done:
                import_orders(st.session_state.uploaded_file)

        if st.session_state.orders and st.session_state.show_send_btn:
            if st.button('🚀 Enviar Pedidos', key='send_orders'):
                    st.session_state.show_dataframes = False
                    st.session_state.show_send_btn = False
                    send_orders(st.session_state.orders)
        
    logging.info('Fim do processo de importacao.')
    logging.info('*********************************************************')
    
if __name__ == '__main__':
    main()