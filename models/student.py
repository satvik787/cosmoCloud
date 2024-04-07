from pydantic import BaseModel

class Address(BaseModel):
    city:str
    country:str

class Student(BaseModel):
    name:str
    age:int
    address:Address



class StudentUpdate(BaseModel):
    name:str | None = None
    age:int | None = None
    address:Address | None = None