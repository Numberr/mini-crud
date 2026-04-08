from pydantic import BaseModel, Field, field_validator, model_validator
from datetime import datetime

class UserBase(BaseModel):
    name: str = Field(min_length=1, max_length=20, examples=['John'])
    lastname: str = Field(min_length=1, max_length=20, examples=['Smith'])

class UserCreate(UserBase):
    password: str = Field(min_length=1, max_length=30)
    birthday: datetime

    @field_validator('birthday')
    def check_min_age(cls, v):
        today = datetime.now()
        age = today.year - v.year - ((today.month, today.day) < (v.month, v.day))
        if age < 10:
            raise ValueError('Возраст должен быть не менее 10 лет')
        return v

class UserResponse(UserBase):
    success: bool
    action_time: datetime
    id: int

class UpdateRequest(BaseModel):
    id: int
    param_to_update: str    = Field(examples=['name', 'lastname', 'birthday', 'password'])
    new_value: str | datetime

    @field_validator('param_to_update')
    def param_check(cls, v):
        if v not in ['name', 'lastname', 'birthday', 'password']:
            raise ValueError('Параметр введен неверно')
        return v
    
    @model_validator(mode='after')
    def check_value(self):
        if self.param_to_update == 'birthday':
            self.new_value = datetime.strptime(self.new_value, '%Y-%m-%d')
        return self
