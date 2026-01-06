
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import text
from sqlalchemy.orm import relationship, sessionmaker
from pydantic import BaseModel

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/api_python"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Pelicula(Base):
    __tablename__="peliculas"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String, index=True)
    director = Column(String)
    anio = Column(Integer)
    
    comentarios = relationship("Comentario", back_populates="pelicula")
    
class Comentario(Base):
    __tablename__="comentarios"
    id = Column(Integer, primary_key=True, index=True)
    contenido = Column(String)
    pelicula_id = Column(Integer, ForeignKey("peliculas.id"))
    
    pelicula = relationship("Pelicula", back_populates="comentarios")

class PeliculaCreate(BaseModel):
    titulo: str
    director: str
    anio: int
    
class PeliculaResponse(PeliculaCreate):
    id: int
    class Config:
        orm_mode = True

class ComentarioCreate(BaseModel):
    contenido: str
    pelicula_id: int
    
class ComentarioResponse(ComentarioCreate):
    id: int
    
    class Config:
        orm_mode = True
        
#gestor de reportes graficos para un sistema de informacion