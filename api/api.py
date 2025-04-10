from fastapi import FastAPI
from pydantic import BaseModel, PositiveInt, EmailStr

app = FastAPI()

class Order(BaseModel):
    index: int
    name: str
    email: EmailStr
    product: str
    quantity: PositiveInt
    unit_value: PositiveInt

@app.post('/api/orders')
def receives_order(order: Order):
    return {'message': 'Pedido recebido com sucesso'}