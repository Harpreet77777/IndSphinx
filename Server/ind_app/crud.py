import math
import subprocess
from datetime import datetime, date, timezone, timedelta, time
from datetime import datetime, date, timedelta, timezone
import asyncio
import os
import pytz
import psycopg2
from sqlalchemy import func
import sqlalchemy
# from dateutil.relativedelta import relativedelta
from fastapi import HTTPException, UploadFile
from sqlalchemy import extract
from sqlalchemy.orm import Session
import aiofiles
from . import models, schemas
import glob
from .thingsboard import TBHelper

sansera_pdf_folder_path = 'D:\\Sansera_pdf_folder'

model_folder_path = '/home/his/ReportServer/SanseraModels'
report_folder_path = '/home/his/ReportServer/SanseraReports'


# ..................................................................................................

async def create_shift_data(db: Session, data: schemas.ShiftDataBase):
    try:
        db_master = models.ShiftData(date_=data.date_, Shift=data.Shift,
                                     machine_name=data.machine_name, Target_Count=data.Target_Count,
                                     Part_Count=data.Part_Count, Rejection_Count=data.Rejection_Count,
                                     OEE=data.OEE, Efficiency=data.Efficiency,
                                     Quality=data.Quality, Availability=data.Availability,
                                     Idle_Time=data.Idle_Time, Breakdown_Time=data.Breakdown_Time,
                                     Breakdown_Count=data.Breakdown_Count, Actual_Target_Count=data.Actual_Target_Count,
                                     Operating_Time=data.Operating_Time, Total_Time=data.Total_Time

                                     )
        db.add(db_master)
        db.commit()
        db.refresh(db_master)
        return db_master
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def get_shift_data(db: Session, date_: date, Shift: schemas.ShiftEnum, machine_name: str):
    try:
        if Shift == 'ALL_SHIFT':
            return db.query(models.ShiftData).filter(models.ShiftData.date_ == date_,
                                                     models.ShiftData.machine_name == machine_name,
                                                     ).all()
        else:

            return db.query(models.ShiftData).filter(models.ShiftData.date_ == date_,
                                                     models.ShiftData.Shift == Shift,
                                                     models.ShiftData.machine_name == machine_name,
                                                     ).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def get_shift_data_(db: Session, date_: date, Shift: schemas.ShiftEnum, machine_name: str):
    try:

        return db.query(models.ShiftData).filter(models.ShiftData.date_ == date_,
                                                 models.ShiftData.Shift == Shift,
                                                 models.ShiftData.machine_name == machine_name,
                                                 ).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def update_shift_data(db: Session, data: schemas.ShiftDataBase):
    try:
        data_db = await get_shift_data_(db, data.date_, data.Shift, data.machine_name)
        mo_id = data_db.id
        db_mo = db.get(models.ShiftData, mo_id)
        for key, value in data.dict(exclude_unset=True).items():
            setattr(db_mo, key, value)
        db.add(db_mo)
        db.commit()
        db.refresh(db_mo)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


# .............................................................................................
async def get_report_shift_data(db: Session, from_date: date, end_date: date, Shift: schemas.ShiftEnum,
                                machine_name: str):
    try:
        if Shift == 'ALL_SHIFT':
            stm = sqlalchemy.select(
                models.ShiftData.date_,
                models.ShiftData.Shift,
                models.ShiftData.Target_Count,
                models.ShiftData.Part_Count,
                models.ShiftData.Rejection_Count,
                models.ShiftData.OEE,
                models.ShiftData.Efficiency,
                models.ShiftData.Quality,
                models.ShiftData.Availability,
                models.ShiftData.Idle_Time,
                models.ShiftData.Breakdown_Time,
                models.ShiftData.Breakdown_Count,
                models.ShiftData.Actual_Target_Count,
                models.ShiftData.Operating_Time,
                models.ShiftData.Total_Time
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_, models.ShiftData.Shift).subquery()
            data = db.query(stm).all()
            result = [
                {
                    'date_': row.date_,
                    'Shift': row.Shift,
                    'Target_Count': row.Target_Count,
                    'Part_Count': row.Part_Count,
                    'Rejection_Count': row.Rejection_Count,
                    'OEE': row.OEE,
                    'Efficiency': row.Efficiency,
                    'Quality': row.Quality,
                    'Availability': row.Availability,
                    'Idle_Time': row.Idle_Time,
                    'Breakdown_Time': row.Breakdown_Time,
                    'Breakdown_Count': row.Breakdown_Count,
                    'Actual_Target_Count': row.Actual_Target_Count,
                    'Operating_Time': row.Operating_Time,
                    'Total_Time': row.Total_Time
                }
                for row in data
            ]
            print(result)
            return result
        else:
            stm = sqlalchemy.select(
                models.ShiftData.date_,
                models.ShiftData.Shift,
                models.ShiftData.Target_Count,
                models.ShiftData.Part_Count,
                models.ShiftData.Rejection_Count,
                models.ShiftData.OEE,
                models.ShiftData.Efficiency,
                models.ShiftData.Quality,
                models.ShiftData.Availability,
                models.ShiftData.Idle_Time,
                models.ShiftData.Breakdown_Time,
                models.ShiftData.Breakdown_Count,
                models.ShiftData.Actual_Target_Count,
                models.ShiftData.Operating_Time,
                models.ShiftData.Total_Time

            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_, models.ShiftData.Shift).subquery()
            data = db.query(stm).all()
            result = [
                {
                    'date_': row.date_,
                    'Shift': row.Shift,
                    'Target_Count': row.Target_Count,
                    'Part_Count': row.Part_Count,
                    'Rejection_Count': row.Rejection_Count,
                    'OEE': row.OEE,
                    'Efficiency': row.Efficiency,
                    'Quality': row.Quality,
                    'Availability': row.Availability,
                    'Idle_Time': row.Idle_Time,
                    'Breakdown_Time': row.Breakdown_Time,
                    'Breakdown_Count': row.Breakdown_Count,
                    'Actual_Target_Count': row.Actual_Target_Count,
                    'Operating_Time': row.Operating_Time,
                    'Total_Time': row.Total_Time
                }
                for row in data
            ]
            print(result)
            return result
    except Exception as e:
        print(e)


async def get_combine_weighted_mean(db: Session, from_date: date, end_date: date, Shift: schemas.ShiftEnum,
                                    machine_name: str):
    try:
        if Shift == 'ALL_SHIFT':
            weighted_mean = {}
            stm_oee = sqlalchemy.select(
                models.ShiftData.OEE * models.ShiftData.Part_Count  # Multiply OEE and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_)

            data_oee = db.execute(stm_oee).fetchall()
            print(data_oee)

            # Calculate the sum of the product of OEE and Part_Count
            total_weighted_oee = sum(row[0] for row in data_oee)

            # Create a dictionary with the total weighted OEE
            result_dict = {
                "total_weighted_oee": total_weighted_oee
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_oee = 0.0
            else:

                weighted_oee = round(result_dict['total_weighted_oee'] / part_count, 2)

            weighted_mean['OEE'] = weighted_oee

            # ..........................Quality...............................

            stm_quality = sqlalchemy.select(
                models.ShiftData.Quality * models.ShiftData.Part_Count  # Multiply Quality and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_)

            data_quality = db.execute(stm_quality).fetchall()
            print(data_quality)

            # Calculate the sum of the product of Quality and Part_Count
            total_weighted_quality = sum(row[0] for row in data_quality)

            # Create a dictionary with the total weighted Quality
            result_dict = {
                "total_weighted_quality": total_weighted_quality
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_quality = 0.0
            else:

                weighted_quality = round(result_dict['total_weighted_quality'] / part_count, 2)

            weighted_mean['Quality'] = weighted_quality

            # ..................................Availibility.........................................

            stm_availability = sqlalchemy.select(
                models.ShiftData.Availability * models.ShiftData.Part_Count  # Multiply Availibility and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_)

            data_availability = db.execute(stm_availability).fetchall()
            print(data_availability)

            # Calculate the sum of the product of Availability and Part_Count
            total_weighted_availability = sum(row[0] for row in data_availability)

            # Create a dictionary with the total weighted Availability
            result_dict = {
                "total_weighted_availability": total_weighted_availability
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_availability = 0.0
            else:

                weighted_availability = round(result_dict['total_weighted_availability'] / part_count, 2)

            weighted_mean['Availability'] = weighted_availability

            # ...................................Efficiency.................................................

            stm_efficiency = sqlalchemy.select(
                models.ShiftData.Efficiency * models.ShiftData.Part_Count  # Multiply Efficiency and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),

                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_)

            data_efficiency = db.execute(stm_efficiency).fetchall()
            print(data_efficiency)

            # Calculate the sum of the product of Efficiency and Part_Count
            total_weighted_efficiency = sum(row[0] for row in data_efficiency)

            # Create a dictionary with the total weighted Efficiency
            result_dict = {
                "total_weighted_efficiency": total_weighted_efficiency
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_efficiency = 0.0
            else:

                weighted_efficiency = round(result_dict['total_weighted_efficiency'] / part_count, 2)

            weighted_mean['Efficiency'] = weighted_efficiency

            # ........................Target Count............................................

            stm_target_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Target_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_target_count = db.query(stm_target_count).first()
            print(data_target_count[0])
            result_target_count = {
                "target_count": data_target_count[0]
            }
            print("Result Target count:", result_target_count)

            weighted_mean['Target_Count'] = result_target_count['target_count']

            # .......................................Part Count................................................
            result_part_count = {
                "part_count": data_part_count[0]
            }

            weighted_mean['Part_Count'] = result_part_count['part_count']

            # ........................................rejection count..........................................

            stm_rejection_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Rejection_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_rejection_count = db.query(stm_rejection_count).first()
            print(data_rejection_count[0])
            result_rejection_count = {
                "rejection_count": data_rejection_count[0]
            }
            print("Result Rejection count:", result_rejection_count)

            weighted_mean['Rejection_Count'] = result_rejection_count['rejection_count']

            # ...............................................Idle Time...................................

            stm_idle_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Idle_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_idle_time = db.query(stm_idle_time).first()
            print(data_idle_time[0])
            result_idle_time = {
                "idle_time": data_idle_time[0]
            }
            print("Result Idle Time:", result_idle_time)

            weighted_mean['Idle_Time'] = result_idle_time['idle_time']

            # ..........................................Breakdown Time...................................

            stm_breakdown_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Breakdown_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_breakdown_time = db.query(stm_breakdown_time).first()
            print(data_breakdown_time[0])
            result_breakdown_time = {
                "breakdown_time": data_breakdown_time[0]
            }
            print("Result Breakdown Time:", result_breakdown_time)

            weighted_mean['Breakdown_Time'] = result_breakdown_time['breakdown_time']

            # .................................................Breakdown Count.....................

            stm_breakdown_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Breakdown_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_breakdown_count = db.query(stm_breakdown_count).first()
            print(data_breakdown_count[0])
            result_breakdown_count = {
                "breakdown_count": data_breakdown_count[0]
            }
            print("Result Breakdown Count:", result_breakdown_count)

            weighted_mean['Breakdown_Count'] = result_breakdown_count['breakdown_count']

            ##.......................Total Time............................................

            stm_total_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Total_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_total_time = db.query(stm_total_time).first()
            print(data_total_time[0])
            result_total_time = {
                "total_time": data_total_time[0]
            }
            print("Result Total Time:", result_total_time)

            weighted_mean['Total_Time'] = result_total_time['total_time']

            ##.......................Operating Time............................................

            stm_operating_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Operating_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_operating_time = db.query(stm_operating_time).first()
            print(data_operating_time[0])
            result_operating_time = {
                "operating_time": data_operating_time[0]
            }
            print("Result Operating Time:", result_operating_time)

            weighted_mean['Operating_Time'] = result_operating_time['operating_time']

            ##.......................Actual Target Count............................................

            stm_actual_tc = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Actual_Target_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.machine_name
            ).subquery()
            data_actual_tc = db.query(stm_actual_tc).first()
            print(data_actual_tc[0])
            result_actual_tc = {
                "actual_tc": data_actual_tc[0]
            }
            print("Result Actual Target Count:", result_actual_tc)

            weighted_mean['Actual_Target_Count'] = result_actual_tc['actual_tc']

            return weighted_mean

        else:

            weighted_mean = {}
            stm_oee = sqlalchemy.select(
                models.ShiftData.OEE * models.ShiftData.Part_Count  # Multiply OEE and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_, models.ShiftData.Shift)

            data_oee = db.execute(stm_oee).fetchall()
            print(data_oee)

            # Calculate the sum of the product of OEE and Part_Count
            total_weighted_oee = sum(row[0] for row in data_oee)

            # Create a dictionary with the total weighted OEE
            result_dict = {
                "total_weighted_oee": total_weighted_oee
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_oee = 0.0
            else:

                weighted_oee = round(result_dict['total_weighted_oee'] / part_count, 2)

            weighted_mean['OEE'] = weighted_oee

            # ..........................Quality...............................

            stm_quality = sqlalchemy.select(
                models.ShiftData.Quality * models.ShiftData.Part_Count  # Multiply Quality and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_, models.ShiftData.Shift)

            data_quality = db.execute(stm_quality).fetchall()
            print(data_quality)

            # Calculate the sum of the product of Quality and Part_Count
            total_weighted_quality = sum(row[0] for row in data_quality)

            # Create a dictionary with the total weighted Quality
            result_dict = {
                "total_weighted_quality": total_weighted_quality
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_quality = 0.0
            else:

                weighted_quality = round(result_dict['total_weighted_quality'] / part_count, 2)

            weighted_mean['Quality'] = weighted_quality

            # ..................................Availibility.........................................

            stm_availability = sqlalchemy.select(
                models.ShiftData.Availability * models.ShiftData.Part_Count  # Multiply Availibility and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_, models.ShiftData.Shift)

            data_availability = db.execute(stm_availability).fetchall()
            print(data_availability)

            # Calculate the sum of the product of Availability and Part_Count
            total_weighted_availability = sum(row[0] for row in data_availability)

            # Create a dictionary with the total weighted Availability
            result_dict = {
                "total_weighted_availability": total_weighted_availability
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_availability = 0.0
            else:

                weighted_availability = round(result_dict['total_weighted_availability'] / part_count, 2)

            weighted_mean['Availability'] = weighted_availability

            # ...................................Efficiency.................................................

            stm_efficiency = sqlalchemy.select(
                models.ShiftData.Efficiency * models.ShiftData.Part_Count  # Multiply Efficiency and Part_Count
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).order_by(models.ShiftData.date_, models.ShiftData.Shift)

            data_efficiency = db.execute(stm_efficiency).fetchall()
            print(data_efficiency)

            # Calculate the sum of the product of Efficiency and Part_Count
            total_weighted_efficiency = sum(row[0] for row in data_efficiency)

            # Create a dictionary with the total weighted Efficiency
            result_dict = {
                "total_weighted_efficiency": total_weighted_efficiency
            }

            print("Result Dictionary:", result_dict)

            stm_part_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Part_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_part_count = db.query(stm_part_count).first()
            part_count = data_part_count[0] if data_part_count and data_part_count[0] else 0

            if part_count == 0:

                weighted_efficiency = 0.0
            else:

                weighted_efficiency = round(result_dict['total_weighted_efficiency'] / part_count, 2)

            weighted_mean['Efficiency'] = weighted_efficiency

            # ........................Target Count............................................

            stm_target_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Target_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_target_count = db.query(stm_target_count).first()
            print(data_target_count[0])
            result_target_count = {
                "target_count": data_target_count[0]
            }
            print("Result Target count:", result_target_count)

            weighted_mean['Target_Count'] = result_target_count['target_count']

            # .......................................Part Count................................................
            result_part_count = {
                "part_count": data_part_count[0]
            }

            weighted_mean['Part_Count'] = result_part_count['part_count']

            # ........................................rejection count..........................................

            stm_rejection_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Rejection_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_rejection_count = db.query(stm_rejection_count).first()
            print(data_rejection_count[0])
            result_rejection_count = {
                "rejection_count": data_rejection_count[0]
            }
            print("Result Rejection count:", result_rejection_count)

            weighted_mean['Rejection_Count'] = result_rejection_count['rejection_count']

            # ...............................................Idle Time...................................

            stm_idle_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Idle_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_idle_time = db.query(stm_idle_time).first()
            print(data_idle_time[0])
            result_idle_time = {
                "idle_time": data_idle_time[0]
            }
            print("Result Idle Time:", result_idle_time)

            weighted_mean['Idle_Time'] = result_idle_time['idle_time']

            # ..........................................Breakdown Time...................................

            stm_breakdown_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Breakdown_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_breakdown_time = db.query(stm_breakdown_time).first()
            print(data_breakdown_time[0])
            result_breakdown_time = {
                "breakdown_time": data_breakdown_time[0]
            }
            print("Result Breakdown Time:", result_breakdown_time)

            weighted_mean['Breakdown_Time'] = result_breakdown_time['breakdown_time']

            # .................................................Breakdown Count.....................

            stm_breakdown_count = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Breakdown_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_breakdown_count = db.query(stm_breakdown_count).first()
            print(data_breakdown_count[0])
            result_breakdown_count = {
                "breakdown_count": data_breakdown_count[0]
            }
            print("Result Breakdown Count:", result_breakdown_count)

            weighted_mean['Breakdown_Count'] = result_breakdown_count['breakdown_count']

            ##.......................Total Time............................................

            stm_total_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Total_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_total_time = db.query(stm_total_time).first()
            print(data_total_time[0])
            result_total_time = {
                "total_time": data_total_time[0]
            }
            print("Result Total Time:", result_total_time)

            weighted_mean['Total_Time'] = result_total_time['total_time']

            ##.......................Operating Time............................................

            stm_operating_time = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Operating_Time),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_operating_time = db.query(stm_operating_time).first()
            print(data_operating_time[0])
            result_operating_time = {
                "operating_time": data_operating_time[0]
            }
            print("Result Operating Time:", result_operating_time)

            weighted_mean['Operating_Time'] = result_operating_time['operating_time']

            ##.......................Actual Target Count............................................

            stm_actual_tc = sqlalchemy.select(
                sqlalchemy.func.sum(models.ShiftData.Actual_Target_Count),
            ).filter(
                models.ShiftData.date_.between(from_date, end_date),
                models.ShiftData.Shift == Shift,
                models.ShiftData.machine_name == machine_name
            ).group_by(
                models.ShiftData.Shift
            ).subquery()
            data_actual_tc = db.query(stm_actual_tc).first()
            print(data_actual_tc[0])
            result_actual_tc = {
                "actual_tc": data_actual_tc[0]
            }
            print("Result Actual Target Count:", result_actual_tc)

            weighted_mean['Actual_Target_Count'] = result_actual_tc['actual_tc']

            return weighted_mean


    except Exception as e:
        print(e)

async def get_report_data(db: Session, date_: date, Shift: schemas.ShiftEnum, machine_name: str):
    try:
        stmt = sqlalchemy.select(
            models.ShiftData.Target_Count,
            models.ShiftData.Part_Count,
            models.ShiftData.Rejection_Count,
            models.ShiftData.OEE,
            models.ShiftData.Efficiency,
            models.ShiftData.Quality,
            models.ShiftData.Availability,
            models.ShiftData.Idle_Time,
            models.ShiftData.Breakdown_Time,
            models.ShiftData.Breakdown_Count,
            models.ShiftData.Actual_Target_Count,
            models.ShiftData.Operating_Time,
            models.ShiftData.Total_Time
        ).filter(
            models.ShiftData.date_ == date_,
            models.ShiftData.machine_name == machine_name
        )

        # Apply shift filter only if not ALL_SHIFT
        if Shift != 'ALL_SHIFT':
            stmt = stmt.filter(models.ShiftData.Shift == Shift)

        data = db.execute(stmt).mappings().all()
        print(data)
        return data

    except Exception as e:
        print(e)



# async def get_report_data(db: Session, date_: date, Shift: schemas.ShiftEnum, machine_name: str):
#     try:
#         if Shift == 'ALL_SHIFT':
#             stm = sqlalchemy.select(
#
#                 models.ShiftData.Target_Count,
#                 models.ShiftData.Part_Count,
#                 models.ShiftData.Rejection_Count,
#                 models.ShiftData.OEE,
#                 models.ShiftData.Efficiency,
#                 models.ShiftData.Quality,
#                 models.ShiftData.Availability,
#                 models.ShiftData.Idle_Time,
#                 models.ShiftData.Breakdown_Time,
#                 models.ShiftData.Breakdown_Count,
#                 models.ShiftData.Actual_Target_Count,
#                 models.ShiftData.Operating_Time,
#                 models.ShiftData.Total_Time
#
#             ).filter(
#                 models.ShiftData.date_ == date_,
#                 models.ShiftData.machine_name == machine_name
#             ).subquery()
#             data = db.query(stm).all()
#             print(data)
#             return data
#         else:
#             stm = sqlalchemy.select(
#
#                 models.ShiftData.Target_Count,
#                 models.ShiftData.Part_Count,
#                 models.ShiftData.Rejection_Count,
#                 models.ShiftData.OEE,
#                 models.ShiftData.Efficiency,
#                 models.ShiftData.Quality,
#                 models.ShiftData.Availability,
#                 models.ShiftData.Idle_Time,
#                 models.ShiftData.Breakdown_Time,
#                 models.ShiftData.Breakdown_Count,
#                 models.ShiftData.Actual_Target_Count,
#                 models.ShiftData.Operating_Time,
#                 models.ShiftData.Total_Time
#
#             ).filter(
#                 models.ShiftData.date_ == date_,
#                 models.ShiftData.Shift == Shift,
#                 models.ShiftData.machine_name == machine_name
#             ).subquery()
#             data = db.execute(stm).mappings().all()
#             print(data)
#             return data
#             # data = db.query(stm).all()
#             # print(data)
#             # return data
#     except Exception as e:
#         print(e)


# ..............................................................................................................

async def get_report_data_by_date_(db: Session, date_: date):
    try:
        result = []

        stm = sqlalchemy.select(

            models.ShiftData.Target_Count,
            models.ShiftData.Part_Count,
            models.ShiftData.Rejection_Count,
            models.ShiftData.OEE,
            models.ShiftData.Efficiency,
            models.ShiftData.Quality,
            models.ShiftData.Availability,
            models.ShiftData.Idle_Time,
            models.ShiftData.Breakdown_Time,
            models.ShiftData.Breakdown_Count,
            models.ShiftData.machine_name,
            models.ShiftData.Shift,
            models.ShiftData.Actual_Target_Count,
            models.ShiftData.Operating_Time,
            models.ShiftData.Total_Time
        ).filter(
            models.ShiftData.date_ == date_
        ).order_by(models.ShiftData.machine_name, models.ShiftData.Shift).subquery()
        data = db.query(stm).all()
        print(data)
        return data
    except Exception as e:
        print(e)


# ....................................................................................................

async def get_report_machine_data(db: Session, date_: date, machine_name: str):
    try:
        stm = sqlalchemy.select(

            models.ShiftData.Target_Count,
            models.ShiftData.Part_Count,
            models.ShiftData.Rejection_Count,
            models.ShiftData.OEE,
            models.ShiftData.Efficiency,
            models.ShiftData.Quality,
            models.ShiftData.Availability,
            models.ShiftData.Idle_Time,
            models.ShiftData.Breakdown_Time,
            models.ShiftData.Breakdown_Count,
            models.ShiftData.Shift,
            models.ShiftData.Actual_Target_Count,
            models.ShiftData.Operating_Time,
            models.ShiftData.Total_Time

        ).filter(
            models.ShiftData.date_ == date_,
            models.ShiftData.machine_name == machine_name
        ).order_by(models.ShiftData.Shift).subquery()
        data = db.query(stm).all()
        print(data)
        return data
    except Exception as e:
        print(e)


async def list_files():
    if os.path.exists(model_folder_path):
        files = await asyncio.to_thread(os.listdir, model_folder_path)
        return {"files": files}
    else:
        return {"message": "Folder does not exist."}


async def download_model(model_name: str):
    if os.path.exists(model_folder_path):
        files = await asyncio.to_thread(os.listdir, model_folder_path)
        if f"{model_name}" in files:
            return os.path.join(model_folder_path, f"{model_name}")
        return {"files": files}
    else:
        return {"message": "Folder does not exist."}


async def upload_report(report_file: UploadFile, line: str, date_: date, shift: str, model_name: str):
    # check filename for variables
    if os.path.exists(report_folder_path):
        files = await asyncio.to_thread(os.listdir, report_folder_path)
        for file_name in files:
            if f"{line}_{date_}_{shift}_{model_name}" in file_name:
                raise HTTPException(status_code=400,
                                    detail=f"Model Report for {date_},{shift},{line},{model_name} already"
                                           f" exists")
        if line in report_file.filename and str(date_) in report_file.filename and \
                shift in report_file.filename and model_name in report_file.filename:
            async with aiofiles.open(os.path.join(report_folder_path, report_file.filename), 'wb') as out_file:
                while content := await report_file.read(1024):  # async read chunk
                    await out_file.write(content)  # async write chunk
            return {"Result": "OK"}
        else:
            raise HTTPException(status_code=400, detail=f"{report_file.filename} is incorrect name for upload.")


async def upload_master(report_file: UploadFile, model_name: str):
    # check filename for variables
    if os.path.exists(model_folder_path):
        if model_name in report_file.filename:
            async with aiofiles.open(os.path.join(model_folder_path, report_file.filename), 'wb') as out_file:
                while content := await report_file.read(1024):  # async read chunk
                    await out_file.write(content)  # async write chunk
            return {"Result": "OK"}
        else:
            raise HTTPException(status_code=400, detail=f"{report_file.filename} is incorrect name for upload.")


async def review_upload(report_file: UploadFile, line: str, date_: date, shift: str, model_name: str):
    # check filename for variables
    if os.path.exists(report_folder_path):
        if line in report_file.filename and str(date_) in report_file.filename and \
                shift in report_file.filename and model_name in report_file.filename:
            async with aiofiles.open(os.path.join(report_folder_path, report_file.filename), 'wb') as out_file:
                while content := await report_file.read(1024):  # async read chunk
                    await out_file.write(content)  # async write chunk
            return {"Result": "OK"}
        else:
            raise HTTPException(status_code=400, detail=f"{report_file.filename} is incorrect name for upload.")


# ********************** New updates **********************************************

async def get_all_report_files(line: str, date_: date, shift: str):
    report_files = []
    if os.path.exists(report_folder_path):
        for file in os.listdir(report_folder_path):
            if file.startswith(f"{line}_{date_.isoformat()}_{shift}") and ".pdf" not in file:
                report_files.append(file)
        return {"report_files": report_files}
    else:
        raise HTTPException(status_code=404, detail={"message": "Folder does not exist."})


async def get_report_file(line: str, date_: date, shift: str, model_name: str):
    if os.path.exists(report_folder_path):
        for file in os.listdir(report_folder_path):
            if file.startswith(f"{line}_{date_.isoformat()}_{shift}_{model_name}") and ".pdf" not in file:
                return file
        return None
    else:
        raise HTTPException(status_code=404, detail={"message": "Folder does not exist."})


async def download_model_review_report(model_name: str, line: str, date_: date, shift: str):
    if os.path.exists(report_folder_path):
        report_file = await get_report_file(line, date_, shift, model_name)
        if report_file:
            return os.path.join(report_folder_path, f"{line}_{date_.isoformat()}_{shift}_{model_name}")
        else:
            raise HTTPException(status_code=404, detail={
                "message": f"File does not exist for {line}_{date_.isoformat()}_{shift}_{model_name}"})
    else:
        return {"message": "Folder does not exist."}


async def download_report_file(model_name: str, line: str, date_: date, shift: str):
    if os.path.exists(report_folder_path):
        # Delete existing PDF files
        existing_files = glob.glob(os.path.join(report_folder_path, "*.pdf"))
        for file_path in existing_files:
            os.remove(file_path)

        report_file = await get_report_file(line, date_, shift, model_name)
        print("models_file-->", report_file)

        # Check if the selected model name exists in the models_files list
        if report_file:
            # Construct the file name based on the provided parameters
            file_name = report_file

            # Check if the file with the constructed name exists in the report folder
            if os.path.exists(os.path.join(report_folder_path, file_name)):
                # Generate the PDF file name
                pdf_file_name = file_name.split(".")[0]
                pdf_file_path = os.path.join(report_folder_path, f"{pdf_file_name}.pdf")

                # Convert the XLS file to PDF using LibreOffice
                # "C:\\Program Files\\LibreOffice\\program\\soffice.exe",
                try:
                    subprocess.run(
                        [
                            "/usr/bin/soffice",
                            "--headless",
                            "--convert-to",
                            "pdf",
                            "--outdir",
                            os.path.dirname(pdf_file_path),
                            os.path.join(report_folder_path, file_name)])
                except Exception as e:
                    raise HTTPException(
                        status_code=500,
                        detail={"message": "Failed to create PDF file."},
                    )

                # Verify if the PDF file was created
                if os.path.exists(pdf_file_path):
                    return pdf_file_path
                else:
                    raise HTTPException(
                        status_code=500,
                        detail={"message": "Failed to create PDF file."},
                    )

            else:
                raise HTTPException(status_code=404, detail={
                    "message": f"File does not exist for {line}_{date_.isoformat()}_{shift}_{model_name}"})
        else:
            raise HTTPException(status_code=404, detail={
                "message": f"File does not exist for {line}_{date_.isoformat()}_{shift}_{model_name}"})
    else:
        raise HTTPException(status_code=404, detail={"message": "Folder does not exist"})


async def reset_password(user_id: str):
    try:
        admin_reset = TBHelper()
        token = admin_reset.reset_password_by_id(reset_id=user_id)

        return {'activated_token': token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


IST = pytz.timezone("Asia/Kolkata")


async def get_hourly_data_old(machine_name: str, date_: date, shift: str):
    try:
        date_from = date_.strftime("%Y-%m-%d")
        date_to = (date_ + timedelta(days=1)).strftime("%Y-%m-%d")

        conn = psycopg2.connect(
            database="thingsboard",
            user="postgres",
            password="Cybershot#903",
            host="localhost",
            port=5432
        )
        cur = conn.cursor()

        cur.execute("SELECT id FROM device WHERE name = %s;", (machine_name,))
        device = cur.fetchone()
        if not device:
            raise HTTPException(status_code=404, detail="Machine not found")

        device_id = device[0]

        # ---------------- SHIFT TIMINGS ----------------
        if shift == "A":
            start_dt = IST.localize(datetime.strptime(f"{date_from} 08:01:00", "%Y-%m-%d %H:%M:%S"))
            end_dt = IST.localize(datetime.strptime(f"{date_from} 20:01:00", "%Y-%m-%d %H:%M:%S"))

            hour_intervals = {
                8: "08:01-09:00", 9: "09:00-10:00", 10: "10:00-11:00",
                11: "11:00-12:00", 12: "12:00-13:00", 13: "13:00-14:00",
                14: "14:00-15:00", 15: "15:00-16:00",
                16: "16:00-17:00", 17: "17:00-18:00",
                18: "18:00-19:00", 19: "19:00-20:00"
            }

        elif shift == "B":
            start_dt = IST.localize(datetime.strptime(f"{date_from} 20:00:00", "%Y-%m-%d %H:%M:%S"))
            end_dt = IST.localize(datetime.strptime(f"{date_to} 08:00:00", "%Y-%m-%d %H:%M:%S"))

            hour_intervals = {
                20: "20:01-21:00", 21: "21:00-22:00", 22: "22:00-23:00",
                23: "23:00-00:00", 0: "00:00-01:00", 1: "01:00-02:00",
                2: "02:00-03:00", 3: "03:00-04:00",
                4: "04:00-05:00", 5: "05:00-06:00",
                6: "06:00-07:00", 7: "07:00-08:00"
            }
        else:
            raise HTTPException(status_code=400, detail="Invalid shift")

        start_ts = int(start_dt.astimezone(timezone.utc).timestamp() * 1000)
        end_ts = int(end_dt.astimezone(timezone.utc).timestamp() * 1000)

        print("START IST:", start_dt)
        print("END IST  :", end_dt)
        print("UNIX TS  :", start_ts, end_ts)

        # ---------------- PART COUNT ----------------
        cur.execute("""
            SELECT
                DATE_TRUNC('hour', timezone('Asia/Kolkata', to_timestamp(ts/1000))) AS hr,
                MIN(COALESCE(long_v, dbl_v)),
                MAX(COALESCE(long_v, dbl_v))
            FROM ts_kv
            WHERE entity_id = %s
              AND key = (SELECT key_id FROM key_dictionary WHERE key='Part_Count' LIMIT 1)
              AND ts >= %s AND ts < %s
            GROUP BY hr
            ORDER BY hr;
        """, (device_id, start_ts, end_ts))

        part_dict = {row[0].hour: (row[1], row[2]) for row in cur.fetchall()}

        # ---------------- BREAKDOWN ----------------
        cur.execute("""
            SELECT
                DATE_TRUNC('hour', timezone('Asia/Kolkata', to_timestamp(ts/1000))) AS hr,
                MIN(COALESCE(long_v, dbl_v)),
                MAX(COALESCE(long_v, dbl_v))
            FROM ts_kv
            WHERE entity_id = %s
              AND key = (SELECT key_id FROM key_dictionary WHERE key='Breakdown_Time' LIMIT 1)
              AND ts >= %s AND ts < %s
            GROUP BY hr
            ORDER BY hr;
        """, (device_id, start_ts, end_ts))

        br_dict = {row[0].hour: (row[1], row[2]) for row in cur.fetchall()}

        # ---------------- MERGE ----------------
        result = []

        for hour, label in hour_intervals.items():
            # Handle date rollover for B shift (00:00–08:00)
            if shift == "B" and hour < 20:
                hour_date = date_ + timedelta(days=1)
            else:
                hour_date = date_

            hour_start = IST.localize(
                datetime.combine(hour_date, time(hour, 0, 0))
            )
            hour_end = hour_start + timedelta(hours=1)

            print(
                f"HOUR SLOT: {label} | "
                f"START: {hour_start} | "
                f"END: {hour_end}"
            )
            part_diff = 0
            break_diff = 0

            if hour in part_dict:
                part_diff = part_dict[hour][1] - part_dict[hour][0]

            if hour in br_dict:
                break_diff = round(br_dict[hour][1] - br_dict[hour][0], 2)

            result.append({
                "hour": label,
                "part_diff": part_diff,
                "break_diff": break_diff
            })

        conn.close()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def upload_pdf_file(report_file: UploadFile, date_: date, shift: str, line: str,
                          machine_name: str):
    # check filename for variables
    if not report_file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Invalid file format. Only PDF files are allowed.")

    pdf_filename = f"{date_}_{shift}_{line}_{machine_name}.pdf"
    if os.path.exists(sansera_pdf_folder_path):
        files = await asyncio.to_thread(os.listdir, sansera_pdf_folder_path)
        for file_name in files:
            if f"{date_}_{shift}_{line}_{machine_name}" in file_name:
                raise HTTPException(status_code=400,
                                    detail=f"Model Report for {date_}_{shift},{line}_{machine_name} already"
                                           f" exists")
        async with aiofiles.open(os.path.join(sansera_pdf_folder_path, pdf_filename), 'wb') as out_file:
            while content := await report_file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk
        return {"Result": "Upload_Successfully"}


async def download_pdf_file(date_: date, shift: str, line: str, machine_name: str):
    pdf_file_name = f"{date_}_{shift}_{line}_{machine_name}.pdf"
    print("pdf_file_name->", pdf_file_name)

    if os.path.exists(sansera_pdf_folder_path):
        files = await asyncio.to_thread(os.listdir, sansera_pdf_folder_path)
        if f"{pdf_file_name}" in files:
            return os.path.join(sansera_pdf_folder_path, pdf_file_name)

        return {"files": files}
    else:
        return {"message": "File does not exist."}


async def get_details_of_upload_files(date_: date, shift: str):
    if os.path.exists(sansera_pdf_folder_path):
        files = await asyncio.to_thread(os.listdir, sansera_pdf_folder_path)
        filtered_files = []
        for file in files:
            file_parts = file.split('_')
            if len(file_parts) == 4 and date.fromisoformat(file_parts[0]) == date_ and file_parts[1] == shift:
                line = file_parts[2]
                machine_name = file_parts[3].split('.')[0]
                file_details = {
                    "file_name": file,
                    "line": line,
                    "machine_name": machine_name
                }
                filtered_files.append(file_details)

        if filtered_files:
            return {"files": filtered_files}
        else:
            return {"message": "No files found matching the criteria"}
    else:
        return {"message": "No file uploaded in the folder"}


########..................................Planned Break..............................................


async def create_planned_break(db: Session, planned_data: schemas.PlannedBreakDataBase):
    db_planned_data = models.PlannedBreakData(**planned_data.dict())
    db.add(db_planned_data)
    db.commit()
    db.refresh(db_planned_data)
    return db_planned_data


async def get_planned_break(db: Session):
    try:
        return db.query(models.PlannedBreakData).order_by(models.PlannedBreakData.id.desc()).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def get_plannned_data_line(db: Session, line: str, machine: str):
    try:
        return db.query(models.PlannedBreakData).filter(models.PlannedBreakData.line == line,
                                                        models.PlannedBreakData.machine == machine
                                                        ).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def update_planned_break(db: Session, planned_data: schemas.PlannedBreakDataBase):
    try:
        db_planned = await get_plannned_data_line(db, planned_data.line, planned_data.machine)
        mo_id = db_planned.id
        db_mo = db.get(models.PlannedBreakData, mo_id)
        for key, value in planned_data.dict(exclude_unset=True).items():
            setattr(db_mo, key, value)
        db.add(db_mo)
        db.commit()
        db.refresh(db_mo)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def get_planned_data_by_line_machine(db: Session, line: str, machine: str):
    try:
        # Attempt to get data for both line and machine
        data = db.query(models.PlannedBreakData).filter(
            models.PlannedBreakData.line == line,
            models.PlannedBreakData.machine == machine
        ).all()

        # Check if data exists for the specific machine
        machine_data_exists = bool(data)

        # If no data found for the specific machine, get data for the line only
        if not machine_data_exists:
            data = db.query(models.PlannedBreakData).filter(
                models.PlannedBreakData.line == line
            ).all()

        return {
            "data": data,
            "machine_data": machine_data_exists
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


########......................................Shift timings............................................


async def create_shift_timings(db: Session, shift_timings: schemas.ShiftTimingsBase):
    formatted_shift_data = {
        "shift_a_start": shift_timings.shift_a_start.strftime("%Y-%m-%d %H:%M:00"),
        "shift_b_start": shift_timings.shift_b_start.strftime("%Y-%m-%d %H:%M:00"),
        "shift_c_start": shift_timings.shift_c_start.strftime("%Y-%m-%d %H:%M:00"),
        "shift_a_end": shift_timings.shift_a_end.strftime("%Y-%m-%d %H:%M:00"),
        "shift_b_end": shift_timings.shift_b_end.strftime("%Y-%m-%d %H:%M:00"),
        "shift_c_end": shift_timings.shift_c_end.strftime("%Y-%m-%d %H:%M:00"),
    }

    db_shift_data = models.ShiftTimings(**formatted_shift_data)
    db.add(db_shift_data)
    db.commit()
    db.refresh(db_shift_data)
    return db_shift_data


async def get_shift(db: Session):
    current_shift_data = db.query(models.ShiftTimings).order_by(models.ShiftTimings.id.desc()).first()
    if current_shift_data:
        shiftAStart = current_shift_data.shift_a_start.time()
        shiftBStart = current_shift_data.shift_b_start.time()
        shiftCStart = current_shift_data.shift_c_start.time()
        shiftAEnd = current_shift_data.shift_a_end.time()
        shiftBEnd = current_shift_data.shift_b_end.time()
        shiftCEnd = current_shift_data.shift_c_end.time()

        now = datetime.now().time()
        new_day = time(23, 59, 59, 999)
        new_one = time(0, 0, 0, 0)
        if shiftBStart <= now < shiftBEnd:
            return 'B'
        elif shiftAStart <= now < shiftAEnd:
            return 'A'
        elif shiftCStart <= now <= new_day or new_one <= now < shiftCEnd:
            return 'C'
        else:
            return 'C'
    else:
        return "No_shift_data"


async def get_shift_details(db: Session):
    current_shift_data = db.query(models.ShiftTimings).order_by(models.ShiftTimings.id.desc()).first()
    if current_shift_data:
        shift_a_start = current_shift_data.shift_a_start.strftime("%H:%M:%S")
        shift_b_start = current_shift_data.shift_b_start.strftime("%H:%M:%S")
        shift_c_start = current_shift_data.shift_c_start.strftime("%H:%M:%S")
        shift_a_end = current_shift_data.shift_a_end.strftime("%H:%M:%S")
        shift_b_end = current_shift_data.shift_b_end.strftime("%H:%M:%S")
        shift_c_end = current_shift_data.shift_c_end.strftime("%H:%M:%S")

        return {
            "shift_a_start": shift_a_start,
            "shift_b_start": shift_b_start,
            "shift_c_start": shift_c_start,
            "shift_a_end": shift_a_end,
            "shift_b_end": shift_b_end,
            "shift_c_end": shift_c_end
        }
    else:
        return {"No shift Data Available.Please Create ShiftData"}


async def delete_shift_details(db: Session):
    try:
        db_shift = db.query(models.ShiftTimings).first()
        if db_shift is None:
            raise HTTPException(status_code=404, detail="Shift Data Not Found")
        shift_id = db_shift.id
        delete_data = models.ShiftTimings.__table__.delete().where(models.ShiftTimings.id == shift_id)

        db.execute(delete_data)
        db.commit()
        return {"detail": "Shift Data Deleted Successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


############.....................................No Plan..........................................


async def calculate_current_date_and_shift(db: Session):
    current_shift_data = db.query(models.ShiftTimings).order_by(models.ShiftTimings.id.desc()).first()

    if current_shift_data:
        shift_a_start = current_shift_data.shift_a_start
        shift_b_start = current_shift_data.shift_b_start
        shift_c_start = current_shift_data.shift_c_start
        shift_a_end = current_shift_data.shift_a_end
        shift_b_end = current_shift_data.shift_b_end
        shift_c_end = current_shift_data.shift_c_end
        now = datetime.now()
        adjusted_current_date = (now - timedelta(hours=shift_a_start.hour, minutes=shift_a_start.minute)).strftime(
            "%Y-%m-%d")
        current_time = now.time()
        new_day = time(23, 59, 59, 999999)
        new_one = time(0, 0, 0, 0)

        if shift_b_start.time() <= current_time < shift_b_end.time():
            current_shift = 'B'
        elif shift_a_start.time() <= current_time < shift_a_end.time():
            current_shift = 'A'
        elif shift_c_start.time() <= current_time <= new_day or new_one <= current_time < shift_c_end.time():
            current_shift = 'C'
        else:
            current_shift = 'C'

        return {
            "current_date": adjusted_current_date,
            "current_shift": current_shift
        }
    else:
        return {
            "current_date": None,
            "current_shift": "No_shift_data"
        }


def calculate_shift_duration(start_time: datetime, end_time: datetime) -> int:
    duration = end_time - start_time
    duration_in_minutes = duration.total_seconds() // 60
    return int(duration_in_minutes)


async def get_duration(db: Session):
    current_shift_data = db.query(models.ShiftTimings).order_by(models.ShiftTimings.id.desc()).first()
    if current_shift_data:
        shift_a_start = current_shift_data.shift_a_start
        shift_b_start = current_shift_data.shift_b_start
        shift_c_start = current_shift_data.shift_c_start
        shift_a_end = current_shift_data.shift_a_end
        shift_b_end = current_shift_data.shift_b_end
        shift_c_end = current_shift_data.shift_c_end

        durationA = calculate_shift_duration(shift_a_start, shift_a_end)
        durationB = calculate_shift_duration(shift_b_start, shift_b_end)
        durationC = calculate_shift_duration(shift_c_start, shift_c_end)

        return {
            "shift_a_start": shift_a_start.strftime("%H:%M:%S"),
            "shift_b_start": shift_b_start.strftime("%H:%M:%S"),
            "shift_c_start": shift_c_start.strftime("%H:%M:%S"),
            "shift_a_end": shift_a_end.strftime("%H:%M:%S"),
            "shift_b_end": shift_b_end.strftime("%H:%M:%S"),
            "shift_c_end": shift_c_end.strftime("%H:%M:%S"),
            "durationA": durationA,
            "durationB": durationB,
            "durationC": durationC
        }
    else:
        return {"No shift Data Available. Please Create ShiftData"}


########## .........................................No Plan...........................................

async def create_no_plan(db: Session, no_planned_data: schemas.NoPlanBase):
    ###########.....# Step 1: Validate no_plan_duration against shift durations...................

    shift_duration = await get_duration(db=db)
    A_duration = shift_duration['durationA']
    B_duration = shift_duration['durationB']
    C_duration = shift_duration['durationC']

    shift = no_planned_data.shift
    no_plan_duration = no_planned_data.no_plan_duration

    if shift == 'A' and no_plan_duration > A_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration A")
    elif shift == 'B' and no_plan_duration > B_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration B")
    elif shift == 'C' and no_plan_duration > C_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration C")

    ########################.........Step 2: Validate against current date and shift..................

    current_status = await calculate_current_date_and_shift(db=db)
    current_date = current_status['current_date']
    current_shift = current_status['current_shift']

    current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

    start_time_date = no_planned_data.start_time.date()

    print(f"Current date: {current_date}, Current shift: {current_shift}")

    shift_order = {'A': 1, 'B': 2, 'C': 3}

    if start_time_date < current_date or (
            start_time_date == current_date and shift_order[no_planned_data.shift] <= shift_order[current_shift]):
        raise HTTPException(status_code=400,
                            detail="Cannot create NoPlan for a past or current shift on the current date")

    #####################........# Step 3: Validate start_time against shift timings.........................

    shift_details = await get_shift_details(db=db)
    start_time = no_planned_data.start_time.time()
    duration = no_planned_data.no_plan_duration

    if shift == 'A':
        shift_start = datetime.strptime(shift_details['shift_a_start'], "%H:%M:%S").time()
        shift_end = datetime.strptime(shift_details['shift_a_end'], "%H:%M:%S").time()
    elif shift == 'B':
        shift_start = datetime.strptime(shift_details['shift_b_start'], "%H:%M:%S").time()
        shift_end = datetime.strptime(shift_details['shift_b_end'], "%H:%M:%S").time()
    elif shift == 'C':
        shift_c_start = datetime.strptime(shift_details['shift_c_start'], "%H:%M:%S").time()
        shift_c_end = datetime.strptime(shift_details['shift_c_end'], "%H:%M:%S").time()

        if not (shift_c_start <= start_time <= time(23, 59, 59) or time(0, 0, 0) <= start_time <= shift_c_end):
            raise HTTPException(status_code=400,
                                detail=f"Start time {start_time} is not within the C shift timings ({shift_c_start} to {shift_c_end})")

    if shift != 'C' and not (shift_start <= start_time <= shift_end):
        raise HTTPException(status_code=400,
                            detail=f"Start time {start_time} is not within the {shift} shift timings ({shift_start} to {shift_end})")

    ################## # Step 4: Validate duration against remaining shift time....................................

    if shift == 'A':
        shift_end_time = datetime.strptime(shift_details['shift_a_end'], "%H:%M:%S").time()
        print(shift_end_time)
    elif shift == 'B':
        shift_end_time = datetime.strptime(shift_details['shift_b_end'], "%H:%M:%S").time()
    elif shift == 'C':
        shift_end_time = datetime.strptime(shift_details['shift_c_end'], "%H:%M:%S").time()
        shift_c_end = datetime.strptime(shift_details['shift_c_end'], "%H:%M:%S").time()
        shift_end_time_seconds = shift_c_end.hour * 3600 + shift_c_end.minute * 60 + shift_c_end.second
        start_time_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second

        if start_time <= shift_c_end:
            difference_minutes = (shift_end_time_seconds - start_time_seconds) / 60
        else:
            difference_minutes = (24 * 3600 - start_time_seconds + shift_end_time_seconds) / 60

        if difference_minutes < duration:
            raise HTTPException(
                status_code=400,
                detail=f"Duration of {duration} minutes is insufficient as it exceeds the time left until shift ends at {shift_c_end}."
            )

    start_time_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
    shift_end_time_seconds = shift_end_time.hour * 3600 + shift_end_time.minute * 60 + shift_end_time.second

    print(start_time_seconds)
    print(shift_end_time_seconds)

    difference_minutes = (shift_end_time_seconds - start_time_seconds) / 60
    if shift != 'C' and (difference_minutes < duration):
        raise HTTPException(
            status_code=400,
            detail=f"Duration of {duration} minutes is insufficient as it exceeds the time left until shift ends at {shift_end_time}."
        )

    ###################.......................Overlapping Condition Check............................................

    existing_no_plans = await get_no_plan_data(db=db, date_=no_planned_data.date_, line=no_planned_data.line,
                                               shift=no_planned_data.shift, machine=no_planned_data.machine)

    no_plan_start_time = no_planned_data.start_time
    no_plan_end_time = no_plan_start_time + timedelta(minutes=no_planned_data.no_plan_duration)

    # Convert to naive datetime if they are aware
    if no_plan_start_time.tzinfo is not None:
        no_plan_start_time = no_plan_start_time.replace(tzinfo=None)
    if no_plan_end_time.tzinfo is not None:
        no_plan_end_time = no_plan_end_time.replace(tzinfo=None)

    for no_plan in existing_no_plans:
        last_start_time = no_plan['start_time']
        last_end_time = no_plan['end_time']

        # Convert to naive datetime if they are aware
        if last_start_time.tzinfo is not None:
            last_start_time = last_start_time.replace(tzinfo=None)
        if last_end_time.tzinfo is not None:
            last_end_time = last_end_time.replace(tzinfo=None)

        print(
            f"Existing NoPlan: {last_start_time.strftime('%Y-%m-%d %H:%M:%S')} to {last_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(
            f"New NoPlan: {no_plan_start_time.strftime('%Y-%m-%d %H:%M:%S')} to {no_plan_end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Check for overlap
        if (no_plan_start_time < last_end_time and no_plan_end_time > last_start_time):
            raise HTTPException(
                status_code=400,
                detail=f"NoPlan overlaps with an existing schedule from {last_start_time.strftime('%Y-%m-%d %H:%M:%S')} to {last_end_time.strftime('%Y-%m-%d %H:%M:%S')}"
            )

    ############....................... Step 5: Save data to database.................................................

    formatted_shift_data = {
        "start_time": no_planned_data.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "date_": no_planned_data.date_,
        "shift": no_planned_data.shift,
        "line": no_planned_data.line,
        "machine": no_planned_data.machine,
        "no_plan_duration": no_planned_data.no_plan_duration

    }
    db_no_planned_data = models.NoPlan(**formatted_shift_data)

    db.add(db_no_planned_data)
    db.commit()
    db.refresh(db_no_planned_data)
    db_no_planned_data.start_time = db_no_planned_data.start_time.strftime("%Y-%m-%d %H:%M:%S")
    return db_no_planned_data


async def get_no_plan_data(db: Session, date_: date, line: str, shift: str, machine: str):
    try:
        results = db.query(models.NoPlan.start_time,
                           models.NoPlan.no_plan_duration).filter(models.NoPlan.date_ == date_,
                                                                  models.NoPlan.line == line,
                                                                  models.NoPlan.shift == shift,
                                                                  models.NoPlan.machine == machine
                                                                  ).all()

        if results:
            no_plan_data = []
            for result in results:
                start_time, no_plan_duration = result
                end_time = start_time + timedelta(minutes=no_plan_duration)
                no_plan_data.append({
                    "no_plan_duration": no_plan_duration,
                    "start_time": start_time,
                    "end_time": end_time
                })
            return no_plan_data
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def get_no_plan_data_update(db: Session, date_: date, line: str, shift: str, machine: str):
    try:
        return db.query(models.NoPlan).filter(models.NoPlan.date_ == date_,
                                              models.NoPlan.line == line,
                                              models.NoPlan.shift == shift,
                                              models.NoPlan.machine == machine
                                              ).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def update_no_plan(db: Session, no_plan: schemas.NoPlanBase):
    db_no_plan = await get_no_plan_data_update(db, no_plan.date_, no_plan.line, no_plan.shift, no_plan.machine)

    shift_duration = await get_duration(db=db)
    A_duration = shift_duration['durationA']
    B_duration = shift_duration['durationB']
    C_duration = shift_duration['durationC']

    shift = no_plan.shift
    no_plan_duration = no_plan.no_plan_duration

    if shift == 'A' and no_plan_duration > A_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration A")
    elif shift == 'B' and no_plan_duration > B_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration B")
    elif shift == 'C' and no_plan_duration > C_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration C")

    current_status = await calculate_current_date_and_shift(db=db)
    current_date = current_status['current_date']
    current_shift = current_status['current_shift']

    current_date = datetime.strptime(current_date, "%Y-%m-%d").date()
    print(f"Current date: {current_date}, Current shift: {current_shift}")

    start_time_date = no_plan.start_time.date()

    print(f"Current date: {current_date}, Current shift: {current_shift}")

    shift_order = {'A': 1, 'B': 2, 'C': 3}
    if start_time_date < current_date or (
            start_time_date == current_date and shift_order[no_plan.shift] <= shift_order[current_shift]):
        raise HTTPException(status_code=400,
                            detail="Cannot create NoPlan for a past or current shift on the current date")

    shift_details = await get_shift_details(db=db)
    start_time = no_plan.start_time.time()

    if shift == 'A':
        shift_start = datetime.strptime(shift_details['shift_a_start'], "%H:%M:%S").time()
        shift_end = datetime.strptime(shift_details['shift_a_end'], "%H:%M:%S").time()
    elif shift == 'B':
        shift_start = datetime.strptime(shift_details['shift_b_start'], "%H:%M:%S").time()
        shift_end = datetime.strptime(shift_details['shift_b_end'], "%H:%M:%S").time()
    elif shift == 'C':
        shift_c_start = datetime.strptime(shift_details['shift_c_start'], "%H:%M:%S").time()
        shift_c_end = datetime.strptime(shift_details['shift_c_end'], "%H:%M:%S").time()

        if not (shift_c_start <= start_time <= time(23, 59, 59) or time(0, 0, 0) <= start_time <= shift_c_end):
            raise HTTPException(status_code=400,
                                detail=f"Start time {start_time} is not within the C shift timings ({shift_c_start} to {shift_c_end})")

    if shift != 'C' and not (shift_start <= start_time <= shift_end):
        raise HTTPException(status_code=400,
                            detail=f"Start time {start_time} is not within the {shift} shift timings ({shift_start} to {shift_end})")

    mo_id = db_no_plan.id
    db_mo = db.get(models.NoPlan, mo_id)
    no_plan.start_time = no_plan.start_time.strftime("%Y-%m-%d %H:%M:%S")
    print(no_plan.start_time)
    for key, value in no_plan.dict(exclude_unset=True).items():
        setattr(db_mo, key, value)
    db.add(db_mo)
    db.commit()
    db.refresh(db_mo)

    db_mo.start_time = db_mo.start_time.strftime("%Y-%m-%d %H:%M:%S")
    return db_mo


async def get_no_plan_duration(db: Session, date_: date, line: str, shift: str, machine: str):
    try:
        results = db.query(
            models.NoPlan.no_plan_duration,
            models.NoPlan.start_time,
            models.NoPlan.date_
        ).filter(
            func.date(models.NoPlan.start_time) == date_,
            models.NoPlan.line == line,
            models.NoPlan.shift == shift,
            models.NoPlan.machine == machine
        ).all()

        if results:
            response = []
            for no_plan_duration, start_time, date_ in results:
                response.append({
                    "date_": date_,
                    "no_plan_duration": no_plan_duration,
                    "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S")
                })
            return response
        else:
            return {"message": "No data found for the given parameters"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


async def get_no_plan_date_range(db: Session, start_date: date, end_date: date, line: str, shift: str, machine: str):
    try:
        results = db.query(
            models.NoPlan
        ).filter(
            func.date(models.NoPlan.start_time).between(start_date, end_date),

            models.NoPlan.line == line,
            models.NoPlan.shift == shift,
            models.NoPlan.machine == machine
        ).all()

        if results:
            return results
        else:
            return {"message": "No data found for the given parameters"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


async def delete_no_plan(id: int, db: Session):
    data = db.query(models.NoPlan).filter(models.NoPlan.id == id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found")

    ########################.........Step 2: Validate against current date and shift..................

    current_status = await calculate_current_date_and_shift(db=db)
    current_date = current_status['current_date']
    current_shift = current_status['current_shift']

    current_date = datetime.strptime(current_date, "%Y-%m-%d").date()

    start_time_date = data.start_time.date()

    print(f"Current date: {current_date}, Current shift: {current_shift}")

    shift_order = {'A': 1, 'B': 2, 'C': 3}

    if start_time_date < current_date or (
            start_time_date == current_date and shift_order[data.shift] <= shift_order[current_shift]):
        raise HTTPException(status_code=400,
                            detail="Cannot delete NoPlan for a past or current shift on the current date")

    print("data", data.id)

    delete_data = models.NoPlan.__table__.delete().where(models.NoPlan.id == id)
    db.execute(delete_data)

    db.commit()
    return {"ok": "deleted successfully"}


def calculate_end_time(start_time: str, duration: int) -> str:
    if isinstance(start_time, datetime):
        start_time_dt = start_time
    elif isinstance(start_time, str):
        start_time_dt = datetime.fromisoformat(start_time)
    else:
        raise ValueError("start_time must be a datetime object or a string")
    end_time_dt = start_time_dt + timedelta(minutes=duration)
    end_time = end_time_dt.isoformat()

    return end_time


async def validate_no_plan(db: Session, no_planned_data: schemas.NoPlanBase):
    # Step 1: Validate no_plan_duration against shift durations
    shift_duration = await get_duration(db=db)
    A_duration = shift_duration['durationA']
    B_duration = shift_duration['durationB']
    C_duration = shift_duration['durationC']

    shift = no_planned_data.shift
    no_plan_duration = no_planned_data.no_plan_duration

    if shift == 'A' and no_plan_duration > A_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration A")
    elif shift == 'B' and no_plan_duration > B_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration B")
    elif shift == 'C' and no_plan_duration > C_duration:
        raise HTTPException(status_code=400,
                            detail="No plan duration is greater than available time in shift duration C")

    shift_details = await get_shift_details(db=db)
    start_time = no_planned_data.start_time.time()
    # Step 2: Validate duration against remaining shift time
    if shift == 'A':
        shift_end_time = datetime.strptime(shift_details['shift_a_end'], "%H:%M:%S").time()
    elif shift == 'B':
        shift_end_time = datetime.strptime(shift_details['shift_b_end'], "%H:%M:%S").time()
    elif shift == 'C':
        shift_end_time = datetime.strptime(shift_details['shift_c_end'], "%H:%M:%S").time()
        shift_c_end = datetime.strptime(shift_details['shift_c_end'], "%H:%M:%S").time()
        shift_end_time_seconds = shift_c_end.hour * 3600 + shift_c_end.minute * 60 + shift_c_end.second
        start_time_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second

        if start_time <= shift_c_end:
            difference_minutes = (shift_end_time_seconds - start_time_seconds) / 60
        else:
            difference_minutes = (24 * 3600 - start_time_seconds + shift_end_time_seconds) / 60

        if difference_minutes < no_plan_duration:
            raise HTTPException(
                status_code=400,
                detail=f"Duration of {no_plan_duration} minutes is insufficient as it exceeds the time left until shift ends at {shift_c_end}."
            )
    start_time_seconds = start_time.hour * 3600 + start_time.minute * 60 + start_time.second
    shift_end_time_seconds = shift_end_time.hour * 3600 + shift_end_time.minute * 60 + shift_end_time.second
    difference_minutes = (shift_end_time_seconds - start_time_seconds) / 60

    if shift != 'C' and (difference_minutes < no_plan_duration):
        raise HTTPException(
            status_code=400,
            detail=f"Duration of {no_plan_duration} minutes is insufficient as it exceeds the time left until shift ends at {shift_end_time}."
        )


async def update_running_no_plan(db: Session, id: int, update_data: schemas.NoPlanUpdate):
    no_plan = db.query(models.NoPlan).filter(models.NoPlan.id == id).first()
    if not no_plan:
        raise HTTPException(status_code=404, detail="NoPlan not found")
    original_start_time = no_plan.start_time
    original_duration = no_plan.no_plan_duration
    original_end_time_str = calculate_end_time(original_start_time, original_duration)
    original_end_time = datetime.fromisoformat(original_end_time_str)
    new_duration = update_data.no_plan_duration
    new_end_time_str = calculate_end_time(original_start_time, new_duration)
    new_end_time = datetime.fromisoformat(new_end_time_str)
    now = datetime.now()
    if not (original_start_time <= now <= original_end_time):
        raise HTTPException(status_code=403, detail="No Plan is not currently running")
    if now > original_end_time:
        raise HTTPException(status_code=403, detail="Cannot update NoPlan for past time on the current date")
    if new_duration < no_plan.no_plan_duration:
        elapsed_time = (now - no_plan.start_time).total_seconds() / 60.0  # Convert seconds to minutes
        if new_duration > elapsed_time:
            no_plan.no_plan_duration = new_duration
            await validate_no_plan(db, no_plan)
            db.commit()
            db.refresh(no_plan)
            return no_plan
        else:
            raise HTTPException(status_code=400,
                                detail="New duration must be greater than the current duration based on elapsed time")
    else:
        overlapping_no_plan = db.query(models.NoPlan).filter(
            models.NoPlan.start_time > no_plan.start_time,  # Next NoPlan starts after the current one
            models.NoPlan.start_time < new_end_time,  # Next NoPlan starts before the new end time
            models.NoPlan.id != no_plan.id  # Exclude the current NoPlan
        ).first()
        if overlapping_no_plan:
            raise HTTPException(status_code=400, detail="New duration overlaps with the next NoPlan")
        no_plan.no_plan_duration = new_duration
        await validate_no_plan(db, no_plan)
        db.commit()
        db.refresh(no_plan)
        return no_plan


############################################################################################


async def get_hourly_data(machine_name: str, date_: date, shift: str):
    try:
        date_from = date_.strftime("%Y-%m-%d")
        date_to = (date_ + timedelta(days=1)).strftime("%Y-%m-%d")

        conn = psycopg2.connect(
            database="thingsboard",
            user="postgres",
            password="Cybershot#903",
            host="localhost",
            port=5432
        )
        cur = conn.cursor()

        # ---------- DEVICE ----------
        cur.execute("SELECT id FROM device WHERE name = %s;", (machine_name,))
        device = cur.fetchone()
        if not device:
            raise HTTPException(status_code=404, detail="Machine not found")

        device_id = device[0]

        # ---------- SHIFT TIMINGS ----------
        if shift == "A":
            start_dt = IST.localize(datetime.strptime(f"{date_from} 06:01:00", "%Y-%m-%d %H:%M:%S"))
            end_dt = IST.localize(datetime.strptime(f"{date_from} 14:00:00", "%Y-%m-%d %H:%M:%S"))

            hour_intervals = {
                6: "06:01-07:00", 7: "07:00-08:00", 8: "08:00-09:00",
                9: "09:00-10:00", 10: "10:00-11:00", 11: "11:00-12:00",
                12: "12:00-13:00", 13: "13:00-14:00"
            }

        elif shift == "B":
            start_dt = IST.localize(datetime.strptime(f"{date_from} 14:01:00", "%Y-%m-%d %H:%M:%S"))
            end_dt = IST.localize(datetime.strptime(f"{date_from} 22:00:00", "%Y-%m-%d %H:%M:%S"))

            hour_intervals = {
                14: "14:01-15:00", 15: "15:00-16:00", 16: "16:00-17:00",
                17: "17:00-18:00", 18: "18:00-19:00", 19: "19:00-20:00",
                20: "20:00-21:00", 21: "21:00-22:00"
            }

        elif shift == "C":
            start_dt = IST.localize(datetime.strptime(f"{date_from} 22:01:00", "%Y-%m-%d %H:%M:%S"))
            end_dt = IST.localize(datetime.strptime(f"{date_to} 06:00:00", "%Y-%m-%d %H:%M:%S"))

            hour_intervals = {
                22: "22:01-23:00", 23: "23:00-00:00",
                0: "00:00-01:00", 1: "01:00-02:00",
                2: "02:00-03:00", 3: "03:00-04:00",
                4: "04:00-05:00", 5: "05:00-06:00"
            }

        else:
            raise HTTPException(status_code=400, detail="Invalid shift")

        # # ---------- SHIFT TIMINGS ----------
        # if shift == "A":
        #     start_dt = IST.localize(datetime.strptime(f"{date_from} 08:01:00", "%Y-%m-%d %H:%M:%S"))
        #     end_dt = IST.localize(datetime.strptime(f"{date_from} 20:00:00", "%Y-%m-%d %H:%M:%S"))
        #
        #     hour_intervals = {
        #         8: "08:01-09:00", 9: "09:00-10:00", 10: "10:00-11:00",
        #         11: "11:00-12:00", 12: "12:00-13:00", 13: "13:00-14:00",
        #         14: "14:00-15:00", 15: "15:00-16:00",
        #         16: "16:00-17:00", 17: "17:00-18:00",
        #         18: "18:00-19:00", 19: "19:00-20:00"
        #     }
        #
        # elif shift == "B":
        #     start_dt = IST.localize(datetime.strptime(f"{date_from} 20:01:00", "%Y-%m-%d %H:%M:%S"))
        #     end_dt = IST.localize(datetime.strptime(f"{date_to} 08:00:00", "%Y-%m-%d %H:%M:%S"))
        #
        #     hour_intervals = {
        #         20: "20:01-21:00", 21: "21:00-22:00", 22: "22:00-23:00",
        #         23: "23:00-00:00", 0: "00:00-01:00", 1: "01:00-02:00",
        #         2: "02:00-03:00", 3: "03:00-04:00",
        #         4: "04:00-05:00", 5: "05:00-06:00",
        #         6: "06:00-07:00", 7: "07:00-08:00"
        #     }
        # else:
        #     raise HTTPException(status_code=400, detail="Invalid shift")

        start_ts = int(start_dt.astimezone(timezone.utc).timestamp() * 1000)
        end_ts = int(end_dt.astimezone(timezone.utc).timestamp() * 1000)

        # ---------- PART COUNT MAX PER HOUR ----------
        cur.execute("""
            SELECT
                DATE_TRUNC('hour', timezone('Asia/Kolkata', to_timestamp(ts/1000))) AS hr,
                MAX(COALESCE(long_v, dbl_v)) AS max_val
            FROM ts_kv
            WHERE entity_id = %s
              AND key = (SELECT key_id FROM key_dictionary WHERE key='Part_Count' LIMIT 1)
              AND ts >= %s AND ts < %s
            GROUP BY hr
            ORDER BY hr;
        """, (device_id, start_ts, end_ts))

        part_dict = {row[0].hour: row[1] for row in cur.fetchall()}

        # ---------- BREAKDOWN TIME MAX PER HOUR ----------
        cur.execute("""
            SELECT
                DATE_TRUNC('hour', timezone('Asia/Kolkata', to_timestamp(ts/1000))) AS hr,
                MAX(COALESCE(long_v, dbl_v)) AS max_val
            FROM ts_kv
            WHERE entity_id = %s
              AND key = (SELECT key_id FROM key_dictionary WHERE key='Breakdown_Time' LIMIT 1)
              AND ts >= %s AND ts < %s
            GROUP BY hr
            ORDER BY hr;
        """, (device_id, start_ts, end_ts))

        br_dict = {row[0].hour: row[1] for row in cur.fetchall()}

        # ---------- HOURLY CALCULATION ----------
        result = []

        prev_part_max = None
        prev_br_max = None

        for hour, label in hour_intervals.items():

            part_diff = 0
            break_diff = 0

            # ---- PART COUNT ----
            if hour in part_dict:

                curr = part_dict[hour]

                if prev_part_max is None:
                    # FIRST HOUR ? use MAX
                    part_diff = curr
                else:
                    part_diff = curr - prev_part_max

                prev_part_max = curr

            # ---- BREAKDOWN ----
            if hour in br_dict:

                curr = br_dict[hour]

                if prev_br_max is None:
                    break_diff = curr
                else:
                    break_diff = curr - prev_br_max

                prev_br_max = curr

            result.append({
                "hour": label,
                "part_diff": max(part_diff, 0),
                "break_diff": round(max(break_diff, 0), 2)
            })

        conn.close()
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
