from pydantic import BaseModel, ValidationError, AfterValidator
from typing import Optional, Annotated


# ---------------------------------------------------------
# Validators (zonder if-statements, met assert)
# ---------------------------------------------------------

def validate_postcode(value: int) -> int:
    # Belgische postcode tussen 1000 en 9999 (voorbeeld)
    assert 1000 <= value <= 9999, "Postcode moet tussen 1000 en 9999 liggen"
    return value

Postcode = Annotated[int, AfterValidator(validate_postcode)]


def validate_student_number(value: str) -> str:
    # Bijv. formaat: S123456
    assert value.startswith("S") and value[1:].isdigit(), "Studentnummer moet bv. S123456 zijn"
    return value

StudentNumber = Annotated[str, AfterValidator(validate_student_number)]


# ---------------------------------------------------------
# Adres Model
# ---------------------------------------------------------

class Address(BaseModel):
    straat: str
    nummer: int
    bus: Optional[str] = None
    postcode: Postcode
    gemeente: str


# ---------------------------------------------------------
# Student Model
# ---------------------------------------------------------

class Student(BaseModel):
    studentennummer: StudentNumber
    geboortedatum: str   # Voor eenvoud; kan ook via validator naar datetime
    adres: Address


# ---------------------------------------------------------
# Registratieprogramma
# ---------------------------------------------------------

def vraag_student():
    print("\n--- Nieuwe student registreren ---")

    try:
        student = Student(
            studentennummer=input("Studentennummer (bv. S123456): "),
            geboortedatum=input("Geboortedatum (YYYY-MM-DD): "),
            adres=Address(
                straat=input("Straat: "),
                nummer=int(input("Huisnummer: ")),
                bus=input("Bus (druk Enter indien geen): ") or None,
                postcode=int(input("Postcode: ")),
                gemeente=input("Gemeente: ")
            )
        )
        return student

    except ValidationError as e:
        print("\n❌ Fout in de gegevens:")
        print(e)
        return None


def main():
    studenten = []

    while True:
        student = vraag_student()

        if student is not None:
            studenten.append(student)
            print("\n✅ Student geregistreerd!")
            print(student)
        
        print("\nNog een student registreren? (j/n): ")
        if input().lower() != "j":
            break

    print("\n--- Overzicht van alle studenten ---")
    for s in studenten:
        print(s)


if __name__ == "__main__":
    main()
