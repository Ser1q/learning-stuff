from pydantic import BaseModel, ValidationError, Field

# basics to play with
class Car(BaseModel):
    id: int 
    model: str
    year: int
    current_year: int = 2026

    def get_car_age(self):
        return self.current_year - self.year 

# exercise
class Address(BaseModel):
    city: str
    street: str

class Student(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50, description="name")
    grade: int = Field(ge=1, le=12, description="grade")
    address: Address

    

if __name__ == "__main__":
    # some_car = Car(id="123", model="Mercedes", year=1998)
    # print(some_car)
    # print(some_car.get_car_age())


    # --- Test Case 1: Valid Data ---
    print("--- TEST 1: Valid Data ---")
    valid_payload = {
        "id": "100",  # String that gets coerced to int
        "name": "Nuradil",
        "grade": "11",
        "address": {
            "city": "Almaty",
            "street": "Abay Ave"
        }
    }

    student = Student(**valid_payload)
    print("Student object:", student)
    print("Dumped as dict:", student.model_dump())

    # --- Test Case 2: Invalid Data (Constraint Violation) ---
    print("\n--- TEST 2: Invalid Data (Should Fail) ---")
    invalid_payload = {
        "id": "not_an_int",
        "name": "A",          # Fails min_length=2
        "grade": 15,           # Fails le=12
        "address": {
            "city": "Astana",
            "street": "Mangilik El"
        }
    }

    try: 
        student = Student(**invalid_payload)
        print("Student object:", student)
        print("Dumped as dict:", student.model_dump())
    except ValidationError as e:
        print(e)
    