from pydantic import BaseModel, PositiveInt, EmailStr

class Order(BaseModel):
    index: int
    name: str
    email: EmailStr
    product: str
    qunatity: PositiveInt
    unit_value: PositiveInt