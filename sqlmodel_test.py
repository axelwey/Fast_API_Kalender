from typing import Optional



from sqlmodel import Field, Session, SQLModel, create_engine



# table=True geeft aan dat deze klasse wordt omgezet naar een databasetabel

# er zijn meer gevorderde scenario's waarin je dit niet wil

class Hero(SQLModel, table=True):

    # hier gebruiken we wel Field omdat we expliciet willen aangeven dat het een primary key is

    id: Optional[int] = Field(default=None, primary_key=True)

    # dit moeten we gewoon declareren

    name: str

    secret_name: str

    age: Optional[int] = None



hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")

hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")

hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

engine = create_engine("sqlite:///database.db")

# dit maakt de nodige tabellen aan voor de subklassen van SQLModel

SQLModel.metadata.create_all(engine)

with Session(engine) as session:

    session.add(hero_1)

    session.add(hero_2)

    session.add(hero_3)

    session.commit() 