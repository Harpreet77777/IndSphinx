from fastapi import Depends
import logging
from fastapi import FastAPI, HTTPException, UploadFile
from datetime import date, datetime
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from . import crud, models, schemas
from fastapi.responses import FileResponse
from .database import SessionLocal, engine
from . import Excel_report
from fastapi import Depends, APIRouter
import os
import asyncio
from pydantic import EmailStr
from enum import Enum
import datetime as dt

models.Base.metadata.create_all(bind=engine)
log = logging.getLogger()
app = FastAPI()
# app = FastAPI(openapi_url="/openapi.json", root_path="/shiv_server")
router = APIRouter()

# uvicorn_access = logging.getLogger("uvicorn.access")
# uvicorn_access.disabled = True

origins = [
    '*'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# model_folder_path = 'D:\\Sansera'
# report_folder_path = 'D:\\SanseraReports'
#
# model_folder_path = '/home/his/ReportServer/SanseraModels'
# report_folder_path = '/home/his/ReportServer/SanseraReports'


model_folder_path = '/root/Sansera/SanseraModels'
report_folder_path = '/root/Sansera/SanseraReports'


@app.post("/create_shift_data/")
async def create_shift_data(data: schemas.ShiftDataBase, db: Session = Depends(get_db)):
    db_graph_data = await crud.get_shift_data_(db, data.date_, data.Shift, data.machine_name
                                              )
    if db_graph_data:
        return await crud.update_shift_data(db=db, data=data)
    return await crud.create_shift_data(db=db, data=data)


@app.get("/get_report_data/{date_}/{Shift}/{machine_name}")
async def get_report_data(date_: date, Shift: schemas.ShiftEnum, machine_name: str, db: Session = Depends(get_db)):
    return await crud.get_report_data(db=db, date_=date_, Shift=Shift, machine_name=machine_name)


@app.get("/get_historical_combined_data/{from_date}/{end_date}/{Shift}/{machine_name}")
async def get_historical_combined_data(from_date: date, end_date: date, Shift: schemas.ShiftEnum, machine_name: str,
                                       db: Session = Depends(get_db)):
    return await crud.get_combine_weighted_mean(db=db, from_date=from_date, end_date=end_date, Shift=Shift,
                                                machine_name=machine_name)


@app.get("/get_report_shift_data/{from_date}/{end_date}/{Shift}/{machine_name}")
async def get_report_shift_data(from_date: date, end_date: date, Shift: schemas.ShiftEnum, machine_name: str,
                                db: Session = Depends(get_db)):
    return await crud.get_report_shift_data(db=db, from_date=from_date, end_date=end_date, Shift=Shift,
                                            machine_name=machine_name)


@app.get("/download_historical_data/{from_date}/{end_date}/{machine_name}/{Shift}", response_class=FileResponse)
async def download_historical_data(from_date: date, end_date: date, machine_name: str, Shift: schemas.ShiftEnum,
                                   db: Session = Depends(get_db)):
    try:
        path_ = await Excel_report.generate_shift_report(db=db, from_date=from_date, end_date=end_date,
                                                         machine_name=machine_name, Shift=Shift)
        log.info(path_)
        return path_
    except Exception as e:
        log.error(e)
        return {"ERROR": str(e)}


@app.get("/generate_report_shift_data/{date_}", response_class=FileResponse)
async def generate_report_shift_data(date_: date, db: Session = Depends(get_db)):
    try:
        path_ = await Excel_report.generate_report_shift_data(db=db, date_=date_)

        log.info(path_)
        return path_
    except Exception as e:
        log.error(e)
        return {"ERROR": str(e)}


@app.get("/generate_report_machine_data/{date_}/{machine_name}", response_class=FileResponse)
async def generate_report_machine_data(date_: date, machine_name: str, db: Session = Depends(get_db)):
    try:
        path_ = await Excel_report.generate_report_machine_data(db=db, date_=date_, machine_name=machine_name)

        log.info(path_)
        return path_
    except Exception as e:
        log.error(e)
        return {"ERROR": str(e)}


@app.get("/generate_daily_report/Sansera_Report_{date_}", response_class=FileResponse)
async def generate_daily_report(date_: date):
    try:
        path_ = Excel_report.generate_daily_report(date_=date_)

        log.info(path_)
        return path_
    except Exception as e:
        log.error(e)
        return {"ERROR": str(e)}


@app.get("/generate_daily_data/{date_}/{shift}/{machine_name}")
async def generate_daily_data(date_: date, shift: str, machine_name: str):
    return Excel_report.generate_daily_data(date_=date_, shift=shift, machine_name=machine_name)


@app.get("/generate_report_downtime/{date_}/{shift}/{machine_name}", response_class=FileResponse)
async def generate_report_downtime(date_: date, shift: str, machine_name: str):
    try:
        path_ = Excel_report.generate_downtime_report(date_=date_, shift=shift, machine_name=machine_name)
        log.info(path_)
        return path_
    except Exception as e:
        log.error(e)
        return {"ERROR": str(e)}


@app.get("/list_files", tags=["Process_Reports"])
async def get_list_files():
    data = await crud.list_files()
    return data


@app.get("/get_models/", tags=["Process_Reports"])
async def get_models():
    model_list = await crud.list_files()
    # model_list = [i.replace(".xls", "") for i in model_list.get('files') if model_list.get('files') is not None]
    return model_list


@app.get("/download_model_file/{model_name}", response_class=FileResponse, tags=["Process_Reports"])
async def download_model_file(model_name: str):
    model_file_path = await crud.download_model(model_name)
    return model_file_path


@app.post("/upload_report/{line}/{date_}/{shift}/{model_name}/", tags=["Process_Reports"])
async def upload_report(report_file: UploadFile, line: str, date_: date, shift: str, model_name: str):
    return await crud.upload_report(report_file, line, date_, shift, model_name)


@app.get("/download_model_report/{line}/{date_}/{shift}/{model_name}", response_class=FileResponse,
         tags=["Process_Reports"])
async def download_report_by_machine(line: str, date_: date, shift: str, model_name: str):
    return await crud.download_report_file(model_name, line, date_, shift)


@app.delete("/master_delete_by_model/{model_name}", tags=["Process_Reports"])
async def master_delete_by_model(model_name: str):
    file_path = os.path.join(model_folder_path, f"{model_name}")
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return {"message": f"File {model_name} deleted successfully."}
        except OSError as e:
            # Failed to delete the file
            raise HTTPException(status_code=500, detail=f"Failed to delete the file: {str(e)}")
    else:
        raise HTTPException(status_code=404, detail=f"File {model_name} does not exist.")


@app.post("/upload_master/{model_name}/", tags=["Process_Reports"])
async def upload_master(report_file: UploadFile, model_name: str):
    return await crud.upload_master(report_file, model_name)


@app.get("/get_all_report_files/{line}/{date_}/{shift}/", tags=["Process_Reports"])
async def get_all_report_files(line: str, date_: date, shift: str):
    file_list = await crud.get_all_report_files(line, date_, shift)
    # file_list = [i.replace(".xls", "") for i in file_list.get('files') if file_list.get('files') is not None]
    return file_list


@app.get("/download_review_report/{line}/{date_}/{shift}/{model_name}", response_class=FileResponse,
         tags=["Process_Reports"])
async def download_review_report(line: str, date_: date, shift: str, model_name: str):
    return await crud.download_model_review_report(model_name, line, date_, shift)


@app.post("/review_upload/{line}/{date_}/{shift}/{model_name}/", tags=["Process_Reports"])
async def review_upload(report_file: UploadFile, line: str, date_: date, shift: str, model_name: str):
    return await crud.review_upload(report_file, line, date_, shift, model_name)


# ******************* New Updates **********************

@app.get("/Admin_reset_password/{user_id}", tags=["ResetPassword"])
async def admin_reset_password(user_id: str):
    return await crud.reset_password(user_id=user_id)


@app.get("/get_hourly_data_old/{machine_name}/{date_}/{shift}")
async def get_hourly_data_old(machine_name: str, date_: date, shift: str):
    return await crud.get_hourly_data_old(machine_name, date_, shift)


@app.get("/get_hourly_data/{machine_name}/{date_}/{shift}")
async def get_hourly_data(machine_name: str, date_: date, shift: str):
    return await crud.get_hourly_data(machine_name, date_, shift)


@app.post("/upload_pdf_file/{date_}/{shift}/{line}/{machine_name}/", tags=["Process_Reports"])
async def upload_pdf_file(report_file: UploadFile, date_: date, shift: str, line: str,
                          machine_name: str):
    return await crud.upload_pdf_file(report_file, date_, shift, line, machine_name)


@app.get("/download_pdf_file/{date_}/{shift}/{line}/{machine_name}/", response_class=FileResponse,
         tags=["Process_Reports"])
async def download_pdf_file(date_: date, shift: str, line: str, machine_name: str):
    pdf_file_path = await crud.download_pdf_file(date_, shift, line, machine_name)
    return pdf_file_path


@app.get("/details_of_upload_files/{date_}/{shift}/", tags=["Process_Reports"])
async def details_of_upload_files(date_: date, shift: str):
    pdf_file_details = await crud.get_details_of_upload_files(date_, shift)
    return pdf_file_details


app.include_router(router)


########....................................Shift timings............................................


@app.post("/create_shift_timings/", tags=["Shift"])
async def create_shift_timings(shift_timings: schemas.ShiftTimingsBase, db: Session = Depends(get_db)):
    return await crud.create_shift_timings(db=db, shift_timings=shift_timings)


@app.get("/get_shift_details/", tags=["Shift"])
async def get_shift_details(db: Session = Depends(get_db)):
    return await crud.get_shift_details(db=db)


@app.get("/get_current_shift/", tags=["Shift"])
async def get_date_and_shift(db: Session = Depends(get_db)):
    shift = await crud.get_shift(db=db)
    time_ = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"shift": shift, "time_": time_}


@app.delete("/delete_shift_data/", tags=['Shift'])
async def delete_shift_details(db: Session = Depends(get_db)):
    return await crud.delete_shift_details(db=db)


#####................................Planned Break...................................


@app.post("/create_planned_break/", tags=["Planned_break"])
async def create_planned_break(planned_data: schemas.PlannedBreakDataCreate, db: Session = Depends(get_db)):
    db_data = await crud.get_plannned_data_line(db, planned_data.line, planned_data.machine)
    if db_data:
        return await crud.update_planned_break(db=db, planned_data=planned_data)
    return await crud.create_planned_break(db=db, planned_data=planned_data)


@app.get("/get_planned_break/", tags=['Planned_break'])
async def get_planned_break(db: Session = Depends(get_db)):
    planned_data = await crud.get_planned_break(db=db)
    return planned_data


@app.get("/get_planned_data_by_line_machine/{line}/{machine}/", tags=['Planned_break'])
async def get_planned_data_by_line_machine(line: str, machine: str, db: Session = Depends(get_db)):
    planned_data = await crud.get_planned_data_by_line_machine(line=line, machine=machine, db=db)
    return planned_data


####.......................................No Plan....................................................

@app.get("/get_shift_duration/", tags=["No Plan"])
async def get_shift_duration(db: Session = Depends(get_db)):
    return await crud.get_duration(db=db)


@app.post("/create_no_plan/", tags=["No Plan"])
async def create_no_plan(no_planned_data: schemas.NoPlanBase, db: Session = Depends(get_db)):
    return await crud.create_no_plan(db=db, no_planned_data=no_planned_data)


@app.get("/get_no_plan_data/{date_}/{shift}/{line}/{machine}/", tags=['No Plan'])
async def get_no_plan_data(date_: date, shift: str, line: str, machine: str, db: Session = Depends(get_db)):
    planned_data = await crud.get_no_plan_duration(date_=date_, shift=shift, line=line, machine=machine, db=db)
    return planned_data


@app.get("/get_no_plan_date_range/{start_date}/{end_date}/{shift}/{line}/{machine}/", tags=['No Plan'])
async def get_no_plan_date_range(start_date: date, end_date: date, shift: str, line: str, machine: str,
                                 db: Session = Depends(get_db)):
    planned_data = await crud.get_no_plan_date_range(start_date=start_date, end_date=end_date, shift=shift, line=line,
                                                     machine=machine, db=db)
    return planned_data


@app.get("/calculate_current_date_and_shift/", tags=["No Plan"])
async def calculate_current_date_and_shift(db: Session = Depends(get_db)):
    return await crud.calculate_current_date_and_shift(db=db)


@app.delete("/delete_no_plan/{id}/", tags=["No Plan"])
async def delete_no_plan(id: int, db: Session = Depends(get_db)):
    return await crud.delete_no_plan(db=db, id=id)


@app.post("/update_running_no_plan/{id}/", tags=["No Plan"])
async def update_running_no_plan(id: int, update_data: schemas.NoPlanUpdate, db: Session = Depends(get_db)):
    return await crud.update_running_no_plan(db=db, id=id, update_data=update_data)
