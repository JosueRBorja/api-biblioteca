from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

#aplicación FastAPI
app = FastAPI(title="API funcionando creador por Sir_JosueRB") 


class Usuario(BaseModel): # Modelo para representar un usuario
    nombre: str
    email: str


class Libro(BaseModel): # Modelo para representar un libro  
    titulo: str
    autor: str


usuarios = [] # Lista para almacenar usuarios
libros = []
contador_usuarios = 1
contador_libros = 1


@app.get("/") # Ruta para la página de inicio
def inicio():
    return {"mensaje": "API funcionando correctamente creador por Sir_JosueRB."} 


@app.post("/usuarios/") # Ruta para crear un nuevo usuario
def crear_usuario(usuario: Usuario):
    global contador_usuarios
    nuevo_usuario = {
        "id": contador_usuarios,
        "nombre": usuario.nombre,
        "email": usuario.email,
    }
    usuarios.append(nuevo_usuario)
    contador_usuarios += 1
    return nuevo_usuario

@app.get("/usuarios/") # Ruta para listar todos los usuarios
def listar_usuarios():
    return usuarios

@app.get("/usuarios/{usuario_id}") # Ruta para obtener un usuario por su ID
def obtener_usuario(usuario_id: int):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.delete("/usuarios/{usuario_id}") # Ruta para eliminar un usuario por su ID
def eliminar_usuario(usuario_id: int):
    for usuario in usuarios:
        if usuario["id"] == usuario_id:
            usuarios.remove(usuario)
            return {"mensaje": "Usuario eliminado"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

@app.post("/libros/") # Ruta para crear un nuevo libro
def crear_libro(libro: Libro):
    global contador_libros
    nuevo_libro = {
        "id": contador_libros,
        "titulo": libro.titulo,
        "autor": libro.autor,
    }
    libros.append(nuevo_libro)
    contador_libros += 1
    return nuevo_libro

@app.get("/libros/") # Ruta para listar todos los libros
def listar_libros():
    return libros

@app.get("/libros/{libro_id}") # Ruta para obtener un libro por su ID
def obtener_libro(libro_id: int):
    for libro in libros:
        if libro["id"] == libro_id:
            return libro
    raise HTTPException(status_code=404, detail="Libro no encontrado")


@app.delete("/libros/{libro_id}") # Ruta para eliminar un libro por su ID
def eliminar_libro(libro_id: int):
    for libro in libros:
        if libro["id"] == libro_id:
            libros.remove(libro)
            return {"mensaje": "Libro eliminado"}
    raise HTTPException(status_code=404, detail="Libro no encontrado")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
