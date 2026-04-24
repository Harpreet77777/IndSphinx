from datetime import date, datetime
from typing import Union, Optional, Dict
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ShiftEnum(str, Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    ALL_SHIFT = 'ALL_SHIFT'


class ShiftDataBase(BaseModel):
    date_: date
    Shift: ShiftEnum
    machine_name: str
    Target_Count: float
    Part_Count: float
    Rejection_Count: float
    OEE: float
    Efficiency: float
    Quality: float
    Availability: float
    Idle_Time: float
    Breakdown_Time: float
    Breakdown_Count: float
    Actual_Target_Count: Optional[float] = None
    Operating_Time: Optional[float] = None
    Total_Time: Optional[float] = None




class ShiftDataCreate(ShiftDataBase):
    pass

    class Config:
        orm_mode = True


class ShiftDataMaster(ShiftDataBase):
    pass

    class Config:
        orm_mode = True


class PlannedBreakDataBase(BaseModel):
    shift_a_planned_break: Dict = {}
    shift_b_planned_break: Dict = {}
    shift_c_planned_break: Dict = {}
    line: str
    machine: str


class PlannedBreakDataCreate(PlannedBreakDataBase):
    pass


class PlannedBreakData(PlannedBreakDataBase):
    id: int

    class Config:
        from_attributes = True


###################....................................................................


class ShiftTimingsBase(BaseModel):
    shift_a_start: datetime
    shift_b_start: datetime
    shift_c_start: datetime
    shift_a_end: datetime
    shift_b_end: datetime
    shift_c_end: datetime


class ShiftTimingsCreate(ShiftTimingsBase):
    pass


class ShiftTimings(ShiftTimingsBase):
    id: int

    class Config:
        from_attributes = True


##########..................................................................................
class NoPlanBase(BaseModel):
    start_time: datetime
    date_: date
    shift: str
    line: str
    machine: str
    no_plan_duration: int


class NoPlanCreate(NoPlanBase):
    pass


class NoPlanUpdate(BaseModel):
    start_time: datetime
    date_: date
    shift: str
    line: str
    machine: str
    no_plan_duration: int

    class Config:
        from_attributes = True


class NoPlan(NoPlanBase):
    id: int

    class Config:
        from_attributes = True
