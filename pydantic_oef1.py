from pydantic import BaseModel, After_validator
from typing import Annotated

def leeftijd_checker(age:int):
    assert 0<age<125 , "oncorrecte leeftijd"
    return age

Age=Annotated[int,After_validator(leeftijd_checker)]