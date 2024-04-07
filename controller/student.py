from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from models.student import Student,StudentUpdate
from bson import ObjectId
router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED)
def insertStudent(req:Request,student:Student):
    res = req.app.db.students.insert_one(student.model_dump())
    return {"id":str(res.inserted_id)}

@router.get("/")
def get(req:Request,country:str | None = None,age:int | None = 0):
    query = {"age":{"$gte":age}}
    if country is not None:
        query = {"address.country":country,"age":{"$gte":age}}
    res = req.app.db.students.find(query,{"name":1,"age":1,"_id":False})
    val = list(res)
    return {"data":val}

@router.get("/{id}")
def getById(req:Request,id:str):
    res = req.app.db.students.find({"_id":ObjectId(id)},{"_id":False})
    res = list(res)
    if len(res) > 0:
        return res[0]
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Student with ID {id} not found")

@router.put("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def update(id: str, req: Request, student: StudentUpdate = Body(...)):
    res = list(req.app.db.students.find({"_id": ObjectId(id)}))
    if len(res) == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {id} not found")
    student = {k: v for k, v in student.model_dump().items() if v is not None}
    if len(student) >= 1:
        res = req.app.db.students.update_one({"_id": ObjectId(id)}, {"$set": student})
    return {}

@router.delete("/{id}")
def delete(request: Request,id: str):
    res = request.app.db.students.delete_one({"_id": ObjectId(id)})
    if res.deleted_count == 1:
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Student with ID {id} not found")

