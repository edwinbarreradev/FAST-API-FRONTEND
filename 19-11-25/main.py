""" # iMPORTAR LAS LIBRERIAS NECESARIAS DE FastApi y sqlalchemy
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware #Importar CORSMidddleware para manejar CORS
from sqlalchemy.orm import Session
from typing import List
from models import Pelicula, PeliculaCreate, PeliculaResponse, Comentario, ComentarioCreate, ComentarioResponse, SessionLocal, Base, engine 

#Crear todas las trablas en la base de datos usando los modelos definidos 
Base.metadata.create_all(bind=engine)

#Inicializar la aplicacion FastrAPI
app = FastAPI()

#Configuracion del middleware de CORS para permitir solicitudes desde diferentes orignes 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #Permitir todos los origenes
    allow_credentials=True,
    allow_methods=["*"], #Permitir todo los metodos HTTP (GET, POST, PUT, DELETE)
    allow_headers=["*"], #PEermitir todos los headers
)

#Funcion para obtener una sesion de base de datos 
def get_db():
    db = SessionLocal() #Crear una nueva sesion de base de datos
    try:
        yield db #Devolver la sesion al consumidor 
    finally:
        db.close() #Cerrar la sesion al final 
        
@app.post("/peliculas/", response_model=PeliculaResponse)
def crear_pelicula(pelicula: PeliculaCreate, db: Session = Depends(get_db)):
    db_pelicula = Pelicula(**pelicula.dict()) #Crear un nuevo objeto Pelicula
    db.add(db_pelicula) #Agregar la pelicula a la sesion
    db.commit() #Confirmar los cambios en la base de datos
    db.refresh(db_pelicula) #Obtener la pelicula recien creada
    return db_pelicula #Devolver la pelicula

#Endpoint para leer todas las peliculas, ordenadas por ID
@app.get("/peliculas/", response_model=List[PeliculaResponse])
def leer_peliculas(db: Session = Depends(get_db)):
    pelicula = db.query(Pelicula).order_by(Pelicula.id).all() #Consultar todas las peliculas y ordenarlas por ID
    return peliculas #Devolver la lista de peliculas 

#Endpoint para leer una pelicula especifica por ID 
@app.get("/peliculas/{pelicula_id}", response_model=PeliculaResponse)
def leer_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    #Buscar la pelicula or ID
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
        #Manejar el caso donde no se encuentra la pelicula
    return pelicula #Devolver la pelicula encontrada 

#EndPont para actualizar 
@app.put("/peliculas/{pelicula_id}", response_model=PeliculaResponse)
def actualizar_pelicula(pelicula_id: int, pelicula: PeliculaCreate, db: Session = Depends(get_db)):
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first() #Buscar la peli por ID
    if db_pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    db_pelicula.titulo = pelicula.titulo #Actualizar el titulo
    db_pelicula.director = pelicula.director #actulizar director
    db_pelicula.anio = pelicula.anio #actualizar año de la peli
    db.commit() #Confirmar los cambios 
    return db_pelicula #Decolcer la pelicula 

#EndPoint para eliminar una pelicula por ID
@app.delete("/peliculas/{pelicula_id}" , response_model=dict)
def eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first() 
    if db_pelicula is None : 
        raise HTTPException(status_code=404, detail="No se encuentra la pelicula")
    db.delete(db_pelicula)
    db.commit()
    return{"detail" : "Pelicula eliminada"} #Devolver un mensaje de exito

#Endpoint para crear un comentario
@app.post("/comentarios/", response_model=ComentarioResponse)
def crear_comentario(comentario: ComentarioCreate, db: Session = Depends(get_db)):
    #Verificar si la pelicula existe
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == comentario.pelicula_id).first()
    if db_pelicula is None : 
        raise HTTPException(status_code=404, detail="Pelicula no encotrada")
    
    #Crear el nuevo comentario
    db_comentario = Comentario(**comentario.dict())
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

@app.get("/peliculas/{pelicula_id}/comentarios", response_model=List[ComentarioResponse])
def leer_comentarios(pelicula_id: int, db: Session = Depends(get_db)):
    #Bsucar la pelicula
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    if db_pelicula is None: 
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    
    #obtener todos los comentarios relacionados con la pelicula
    return db_pelicula.comentarios #Devolver la lista de comentarios 

#Endpoint para leer todo slos comentarios**
@app.get("/comentarios/", response_model=List[ComentarioResponse])
def leer_comentarios_all(db: Session = Depends(get_db)):
    #Obtener todos los comentairos de todas las peliculas 
    comentarios = db.query(Comentario).all()
    return comentarios # devolver la lista de todos los comentarios 

#Endpoint par actualizar  un comentarios existente 
@app.put("/comentarios/{comentario_id}", response_model=ComentarioResponse)
def actualzar_comentario(comentario_id: int, comentario: ComentarioCreate, db: Session = Depends(get_db)):
    db_comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if db_comentario is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    
    #Verificar si la pelicula asociada al comentario existe
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == comentario.pelicula.id).first()
    if db_pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    
    #Actualizar el contenido del comentario y el ID de la pelicula
    db_comentario.contenido = comentario.contenido
    db_comentario.pelicula_id = comentario.pelicula_id
    
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

#ENDpoint para elimianr u comentario 
@app.delete("/comentarios/{comentario_id}", response_model=dict)
def eliminar_comentario(comentario_id : int, db: Session = Depends(get_db)):
    db_comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if db_comentario is None:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    db.delete(db_comentario) #Eliminar el comentario 
    db.commit()
    return {"detail" : "Comentario eliminado"} #mensaje de exito  """
    
    # Importar las librerias necesarias de FastAPI y SQLAlchemy
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from models import Pelicula, PeliculaCreate, PeliculaResponse, Comentario, ComentarioCreate, ComentarioResponse, SessionLocal, Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        
@app.post("/peliculas/", response_model=PeliculaResponse)
def crear_pelicula(pelicula: PeliculaCreate, db: Session = Depends(get_db)):
    from sqlalchemy import text
    sql_function_call = text("""
        SELECT id, titulo, director, anio FROM insert_pelicula(:titulo, :director, :anio);
    """)
    try:
        result = db.execute(
            sql_function_call,
            {
                "titulo": pelicula.titulo,
                "director": pelicula.director,
                "anio": pelicula.anio
            }
        ).fetchone() 

        if result is None:
            raise HTTPException(status_code=500, detail="Fallo al insertar la película a través de la función SQL.")
        db.commit() 
        return result._mapping
        
    except Exception as e:
        db.rollback() 
        raise HTTPException(status_code=400, detail=f"Error en la base de datos al crear película: {e}")

@app.get("/peliculas/", response_model=List[PeliculaResponse])
def leer_peliculas(db: Session = Depends(get_db)):
    peliculas = db.query(Pelicula).order_by(Pelicula.id).all()
    return peliculas

@app.get("/peliculas/{peliculas_id}", response_model=PeliculaResponse)
def leer_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    if pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    return pelicula

@app.put("/peliculas/{pelicula_id}",response_model=PeliculaResponse)
def actualizar_pelicula(pelicula_id: int, pelicula: PeliculaCreate, db: Session = Depends(get_db)):
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    if db_pelicula is None:
        raise HTTPException(status_code=404, detail="Pelicula no encontrada")
    db_pelicula.titulo = pelicula.titulo
    db_pelicula.director = pelicula.director
    db_pelicula.anio = pelicula.anio
    db.commit()
    return db_pelicula

@app.delete("/peliculas/{pelicula_id}", response_model=dict)
def eliminar_pelicula(pelicula_id: int, db: Session = Depends(get_db)):
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    if db_pelicula is None:
        raise HTTPException(status_code = 404, detail = "Pelicula no encontrada")
    db.delete(db_pelicula)
    db.commit()
    return{"detail":"Pelicula eliminada"}

@app.post("/comentarios/", response_model=ComentarioResponse)
def crear_comentario(comentario: ComentarioCreate, db: Session = Depends(get_db)):
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == comentario.pelicula_id).first()
    if db_pelicula is None:
        raise HTTPException(status_code = 404, detail="Pelicula no encontrada")

    db_comentario = Comentario(**comentario.dict())
    db.add(db_comentario)
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

@app.get("/peliculas/{pelicula_id}/comentarios", response_model = List[ComentarioResponse])
def leer_comentarios(pelicula_id: int, db: Session = Depends(get_db)):
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == pelicula_id).first()
    if db_pelicula is None:
        raise HTTPException(status_code = 404, detail = "Pelicula no encontrada")
    return db_pelicula.comentarios

@app.get("/comentarios/", response_model=List[ComentarioResponse])
def leer_comentarios_all(db: Session = Depends(get_db)):
    comentarios = db.query(Comentario).all()
    return comentarios

@app.put("/comentarios/{comentario_id}", response_model=ComentarioResponse)
def actualizar_comentario(comentario_id: int, comentario: ComentarioCreate, db: Session = Depends(get_db)):
    db_comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if db_comentario is None:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    
    db_pelicula = db.query(Pelicula).filter(Pelicula.id == comentario.pelicula_id).first()
    if db_pelicula is None:
        raise HTTPException(status_code = 404, detail = "Pelicula no encontrada")
    
    db_comentario.contenido = comentario.contenido
    db_comentario.pelicula_id = comentario.pelicula_id
    
    db.commit()
    db.refresh(db_comentario)
    return db_comentario

@app.delete("/comentarios/{comentario_id}", response_model=dict)
def eliminar_comentario(comentario_id: int, db: Session = Depends(get_db)):
    db_comentario = db.query(Comentario).filter(Comentario.id == comentario_id).first()
    if db_comentario is None:
        raise HTTPException(status_code=404, detail="Comentario no encontrado")
    db.delete(db_comentario)
    db.commit()
    return{"detail":"Comentario Eliminado"}