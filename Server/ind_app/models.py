from sqlalchemy import Column, Integer, String, Float, Date, JSON, DateTime
from datetime import datetime
from .database import Base


class ShiftData(Base):
    __tablename__ = "shiftdata"

    id = Column(Integer, primary_key=True, index=True)

    date_ = Column(Date)
    Shift = Column(String)
    machine_name = Column(String)
    Target_Count = Column(Float)
    Part_Count = Column(Float)
    Rejection_Count = Column(Float)
    OEE = Column(Float)
    Efficiency = Column(Float)
    Quality = Column(Float)
    Availability = Column(Float)
    Idle_Time = Column(Float)
    Breakdown_Time = Column(Float)
    Breakdown_Count = Column(Float)
    Actual_Target_Count = Column(Float, default=None, nullable = True)
    Operating_Time = Column(Float, default=None, nullable = True)
    Total_Time = Column(Float, default=None, nullable = True)


class ShiftTimings(Base):
    __tablename__ = "shift_timings"

    id = Column(Integer, primary_key=True, index=True)
    shift_a_start = Column(DateTime)
    shift_b_start = Column(DateTime)
    shift_c_start = Column(DateTime)
    shift_a_end = Column(DateTime)
    shift_b_end = Column(DateTime)
    shift_c_end = Column(DateTime)


class PlannedBreakData(Base):
    __tablename__ = 'plannedbreak_data'

    id = Column(Integer, primary_key=True, index=True)
    shift_a_planned_break = Column(JSON, default={})
    shift_b_planned_break = Column(JSON, default={})
    shift_c_planned_break = Column(JSON, default={})
    line = Column(String)
    machine = Column(String)


class NoPlan(Base):
    __tablename__ = "no_plan"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime)
    date_ = Column(Date)
    shift = Column(String)
    line = Column(String)
    machine = Column(String)
    no_plan_duration = Column(Integer)
