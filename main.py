from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
import uvicorn

#aplicación FastAPI
app = FastAPI(title="API funcionando creado por Sir_JosueRB") 


class Usuario(SQLModel, table=True): # Clase para la tabla de usuarios
    id: int | None = Field(default=None, primary_key=True)
    nombre: str
    email: str


class Libro(SQLModel, table=True): # Clase para la tabla de libros
    id: int | None = Field(default=None, primary_key=True)
    titulo: str
    autor: str


engine = create_engine( # Creación del motor de base de datos SQLite
    "sqlite:///database.db",
    connect_args={"check_same_thread": False},
)
SQLModel.metadata.create_all(engine)


@app.get("/") # Ruta para la página de inicio
def inicio():
    return {"mensaje": "API funcionando correctamente creado por Sir_JosueRB."} 


@app.post("/usuarios/") # Ruta para crear un nuevo usuario
def crear_usuario(usuario: Usuario):
    usuario.id = None
    with Session(engine) as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

@app.get("/usuarios/") # Ruta para listar todos los usuarios
def listar_usuarios():
    with Session(engine) as session:
        return session.exec(select(Usuario)).all()

@app.get("/usuarios/{usuario_id}") # Ruta para obtener un usuario por su ID
def obtener_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return usuario

@app.put("/usuarios/{usuario_id}") # Ruta para actualizar un usuario
def actualizar_usuario(usuario_id: int, datos: Usuario):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        usuario.nombre = datos.nombre
        usuario.email = datos.email
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario

@app.delete("/usuarios/{usuario_id}") # Ruta para eliminar un usuario por su ID
def eliminar_usuario(usuario_id: int):
    with Session(engine) as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        session.delete(usuario)
        session.commit()
        return {"mensaje": "Usuario eliminado"}

@app.post("/libros/") # Ruta para crear un nuevo libro
def crear_libro(libro: Libro):
    libro.id = None
    with Session(engine) as session:
        session.add(libro)
        session.commit()
        session.refresh(libro)
        return libro

@app.get("/libros/") # Ruta para listar todos los libros
def listar_libros():
    with Session(engine) as session:
        return session.exec(select(Libro)).all()

@app.get("/libros/{libro_id}") # Ruta para obtener un libro por su ID
def obtener_libro(libro_id: int):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        return libro

@app.put("/libros/{libro_id}") # Ruta para actualizar un libro
def actualizar_libro(libro_id: int, datos: Libro):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        libro.titulo = datos.titulo
        libro.autor = datos.autor
        session.add(libro)
        session.commit()
        session.refresh(libro)
        return libro


@app.delete("/libros/{libro_id}") # Ruta para eliminar un libro por su ID
def eliminar_libro(libro_id: int):
    with Session(engine) as session:
        libro = session.get(Libro, libro_id)
        if not libro:
            raise HTTPException(status_code=404, detail="Libro no encontrado")
        session.delete(libro)
        session.commit()
        return {"mensaje": "Libro eliminado"}


if __name__ == "__main__": 
    uvicorn.run(app, host="0.0.0.0", port=8000)
