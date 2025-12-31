from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from data_interactor import Datainteractor, ContactHandling


class Contact(BaseModel):
    first_name: str
    last_name: str
    phone_number: str


app = FastAPI()


@app.get("/contacts")
def get_all_contacts():
    try:
        return Datainteractor.get_all_contacts()
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


@app.post("/contacts")
def create_contact(contact: Contact):
    try:
        cont = ContactHandling(
            contact.first_name, contact.last_name, contact.phone_number
        )

        contact_id = Datainteractor.create_contact(cont.convert_to_dict())

        return {"message": "Contact successfully created", "id": contact_id}

    except Exception as error:
        raise HTTPException(status_code=500, detail="Contact database is not available")


@app.put("/contacts/{contact_id}")
def update_contact(contact_id: str, contact: Contact):
    cont = ContactHandling(contact.first_name, contact.last_name, contact.phone_number)

    updated = Datainteractor.update_contact(contact_id, cont.convert_to_dict())

    if not updated:
        raise HTTPException(
            status_code=404, detail="Contact not found or update failed"
        )

    return {"message": "Contact updated successfully"}


@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: str):
    deleted = Datainteractor.delete_contact(contact_id)

    if not deleted:
        raise HTTPException(
            status_code=404, detail="Contact not found or delete failed"
        )

    return {"message": "Contact deleted successfully"}

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="localhost",port=8000)
