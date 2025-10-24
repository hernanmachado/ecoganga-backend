from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, db
from pathlib import Path
from typing import List, Optional
from pydantic import BaseModel
import pandas as pd

# --------------------
# Pydantic Schemas
# --------------------
class PromocionBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria: str
    comercio_id: int

class PromocionCreate(PromocionBase):
    pass

class Promocion(PromocionBase):
    id: int
    class Config:
        from_attributes = True

# --------------------
# App Config
# --------------------
app = FastAPI(title="Ecoganga Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=db.engine)

def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

# --------------------
# COMERCIOS CRUD
# --------------------
@app.get("/comercios/")
def listar_comercios(db: Session = Depends(get_db)):
    return db.query(models.Comercio).all()

@app.post("/comercios/")
def crear_comercio(c: dict, db: Session = Depends(get_db)):
    nuevo = models.Comercio(**c)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.put("/comercios/{comercio_id}")
def actualizar_comercio(comercio_id: int, data: dict, db: Session = Depends(get_db)):
    c = db.query(models.Comercio).filter_by(id=comercio_id).first()
    if not c:
        return {"error": "Comercio no encontrado"}
    for k, v in data.items():
        setattr(c, k, v)
    db.commit()
    db.refresh(c)
    return c

@app.delete("/comercios/{comercio_id}")
def eliminar_comercio(comercio_id: int, db: Session = Depends(get_db)):
    c = db.query(models.Comercio).filter_by(id=comercio_id).first()
    if not c:
        return {"error": "Comercio no encontrado"}
    db.delete(c)
    db.commit()
    return {"ok": True}

# --------------------
# PROMOCIONES CRUD
# --------------------
@app.get("/promociones/", response_model=List[Promocion])
def listar_promociones(categoria: Optional[str] = None, db: Session = Depends(get_db)):
    q = db.query(models.Promocion)
    if categoria and categoria != "Todas":
        q = q.filter(models.Promocion.categoria == categoria)
    return q.all()

@app.post("/promociones/", response_model=Promocion)
def crear_promocion(promo: PromocionCreate, db: Session = Depends(get_db)):
    nueva = models.Promocion(**promo.dict())
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.put("/promociones/{promo_id}")
def actualizar_promocion(promo_id: int, data: dict, db: Session = Depends(get_db)):
    p = db.query(models.Promocion).filter_by(id=promo_id).first()
    if not p:
        return {"error": "Promoción no encontrada"}
    for k, v in data.items():
        setattr(p, k, v)
    db.commit()
    db.refresh(p)
    return p

@app.delete("/promociones/{promo_id}")
def eliminar_promocion(promo_id: int, db: Session = Depends(get_db)):
    p = db.query(models.Promocion).filter_by(id=promo_id).first()
    if not p:
        return {"error": "Promoción no encontrada"}
    db.delete(p)
    db.commit()
    return {"ok": True}

# --------------------
# SEEDING DATA
# --------------------
@app.post("/seed")
def seed_comercios(db: Session = Depends(get_db)):
    comercios = [
        {"nombre": "Dietética Natural", "tipo": "dietetica", "direccion": "Av. Corrientes 1234", "latitud": -34.598, "longitud": -58.420, "telefono": "11-1234-5678", "email": "info@natural.com", "horario": "Lun-Sab 9:00-20:00"},
        {"nombre": "Super Salud", "tipo": "supermercado", "direccion": "Av. Santa Fe 2345", "latitud": -34.588, "longitud": -58.395, "telefono": "11-2345-6789", "email": "contacto@supersalud.com", "horario": "Lun-Dom 8:00-22:00"}
    ]
    for c in comercios:
        db.add(models.Comercio(**c))
    db.commit()
    return {"message": "Comercios cargados"}

@app.post("/seed_promociones")
def seed_promos(db: Session = Depends(get_db)):
    promos = [
        {"nombre": "Mix Frutos Secos", "descripcion": "250g mix premium", "precio": 1200, "categoria": "vegano", "comercio_id": 1},
        {"nombre": "Pan Sin Gluten", "descripcion": "Pan artesanal", "precio": 800, "categoria": "gluten_free", "comercio_id": 2}
    ]
    for p in promos:
        db.add(models.Promocion(**p))
    db.commit()
    return {"message": "Promociones cargadas"}


