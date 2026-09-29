from typing import Self
from pydantic import field_validator
from pydantic import functional_validators
from email import charset
import email
from pydantic import Field
from pydantic import BaseModel, ConfigDict, ValidationError, field_validator, model_validator

class StaffRegistration(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    full_name: str = Field(min_length=3, max_length=256)
    email: str
    role: str
    password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)

    @field_validator("email")
    @classmethod
    def email_end(cls, value: str) -> str:
        if not value.endswith("@todayschool.kz"):
            raise ValueError("Incorrect email format, use @todayschool.kz!")
        return value

    @field_validator("full_name", mode="after")
    @classmethod
    def full_name_format(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned.split()) > 5:
            raise ValueError("Too much words")
        return cleaned

    @field_validator("role", mode="after")
    @classmethod
    def available_roles(cls, value: str) -> str:
        cleaned = value.lower().strip()
        if cleaned not in ["teacher", "om", "admin"]:
            raise ValueError("Role is invalid!")
        return cleaned

    @model_validator(mode="after")
    def check_password_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match!")
        return self
        
if __name__ == "__main__":
    # Test 
    try:
        demo_staff = StaffRegistration(full_name="Arman Madi", email="arman.madi@todayschool.kz", role="teacher", password="qwerty12345", confirm_password="qwerty12345")
        print(demo_staff)
    except ValidationError as e:
        print(e)

    try:
        ivan_gangsta = StaffRegistration(full_name="Ivan Din", email="vanya.din@gmail.com", role="gangsta", password="qwerty12345", confirm_password="qwerty12345")
        print(ivan_gangsta, "\n")
    except ValidationError as e:
        print(e)

    try:
        ivan_gangsta = StaffRegistration(full_name="Ivan Din", email="vanya.di@todayschool.kz", role="gangsta", password="qwerty12345", confirm_password="qwerty12345")
        print(ivan_gangsta, "\n")
    except ValidationError as e:
        print(e)

    try:
        ivan_gangsta = StaffRegistration(full_name="Ivan Din", email="vanya.di@todayschool.kz", role="om", password="qerty12345", confirm_password="qwerty12345")
        print(ivan_gangsta, "\n")
    except ValidationError as e:
        print(e)

    try:
        demo_staff = StaffRegistration(full_name="Arman Madi", email="arman.madi@todayschool.kz", role="teacher", password="qwerty12345", confirm_password="qwerty12345", admin="true")
        print(demo_staff, "\n")
    except ValidationError as e:
        print(e)
        

         

    

