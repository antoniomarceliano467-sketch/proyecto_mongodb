from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from bson import ObjectId
from pymongo import MongoClient
from datetime import datetime
import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

# 1. INICIALIZACIÓN DE LA API Y SEGURIDAD (CORS)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite que tu HTML se conecte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. CONEXIÓN A MONGODB ATLAS
uri = "mongodb+srv://Antonio_Marceliano:SoldierMaggot45@cluster1.wlqnuf6.mongodb.net/"
cliente = MongoClient(uri)
db = cliente["sistema_rag"]  # Nombre de tu base de datos principal

# 3. CONFIGURACIÓN DE CORREO SMTP (GMAIL)
EMAIL_REMITENTE = "antoniomarceliano467@gmail.com"
EMAIL_PASSWORD = "nlxfeqcjvduifgxz"  # 16 caracteres sin espacios

def enviar_codigo_correo(destinatario: str, codigo: str):
    asunto = "Código de Verificación - STI RAG"
    cuerpo = f"Hola, bienvenido al Panel Administrativo RAG.\n\nTu código de verificación OTP es: {codigo}\n\nIngrésalo en la plataforma para completar tu registro."
    
    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMITENTE
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(cuerpo, 'plain'))
    
    try:
        # Añadimos timeout=5 para evitar que Render congele el servidor
        server = smtplib.SMTP('smtp.gmail.com', 587, timeout=5)
        server.starttls()
        server.login(EMAIL_REMITENTE, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Aviso SMTP (Bloqueado por Render Cloud): {e}")
        return False

@app.post("/solicitar-codigo")
async def solicitar_codigo(correo: str, password: str):
    codigo_otp = str(random.randint(100000, 999999))
    coleccion_usuarios = db["usuarios"]
    
    coleccion_usuarios.update_one(
        {"correo": correo}, 
        {"$set": {"codigo": codigo_otp, "verificado": False, "password": password}}, 
        upsert=True
    )
    
    exito = enviar_codigo_correo(correo, codigo_otp)
    
    # Si Render bloquea el puerto SMTP, permitimos continuar enviando el mensaje de éxito
    # para que puedas ver el código en tu base de datos o consola y avanzar con la prueba.
    return {
        "mensaje": "Código generado exitosamente",
        "codigo_respaldo": codigo_otp 
    }
# ==========================================
# 4. RUTAS PARA MOSTRAR EL FRONTEND (HTML)
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def mostrar_inicio():
    with open("login.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/login.html", response_class=HTMLResponse)
async def mostrar_login():
    with open("login.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard.html", response_class=HTMLResponse)
async def mostrar_dashboard():
    with open("dashboard.html", "r", encoding="utf-8") as f:
        return f.read()

# ==========================================
# RUTAS DE AUTENTICACIÓN (LOGIN Y REGISTRO)
# ==========================================

@app.post("/login")
async def iniciar_sesion(correo: str, password: str):
    coleccion_usuarios = db["usuarios"]
    usuario = coleccion_usuarios.find_one({"correo": correo, "password": password})
    
    if not usuario:
        return {"error": "Correo o contraseña incorrectos. Acceso denegado."}
    
    if not usuario.get("verificado", False):
        return {"error": "Cuenta no verificada. Por favor, solicita y valida tu código de correo."}
        
    return {"mensaje": "Inicio de sesión exitoso"}

@app.post("/solicitar-codigo")
async def solicitar_codigo(correo: str, password: str):
    codigo_otp = str(random.randint(100000, 999999))
    coleccion_usuarios = db["usuarios"]
    
    coleccion_usuarios.update_one(
        {"correo": correo}, 
        {"$set": {"codigo": codigo_otp, "verificado": False, "password": password}}, 
        upsert=True
    )
    
    exito = enviar_codigo_correo(correo, codigo_otp)
    if exito:
        return {"mensaje": "Código enviado exitosamente"}
    else:
        return {"error": "Error al enviar el correo."}

@app.post("/verificar-codigo")
async def verificar_codigo(correo: str, codigo_ingresado: str):
    coleccion_usuarios = db["usuarios"]
    usuario = coleccion_usuarios.find_one({"correo": correo})
    
    if not usuario:
        return {"error": "Usuario no encontrado"}
        
    if usuario.get("codigo") == codigo_ingresado:
        coleccion_usuarios.update_one({"correo": correo}, {"$set": {"verificado": True}})
        return {"mensaje": "Cuenta verificada correctamente."}
    else:
        return {"error": "Código incorrecto."}


# ==========================================
# RUTAS DEL CRUD (GESTIÓN DE ESTUDIANTES)
# ==========================================

@app.get("/estudiantes")
async def obtener_estudiantes():
    coleccion_est = db["estudiantes"]
    lista = []
    for est in coleccion_est.find():
        est["_id"] = str(est["_id"])
        lista.append(est)
    return {"estudiantes": lista}

@app.post("/insertar-estudiante")
async def insertar_estudiante(
    nombre: Optional[str] = None,
    matricula: Optional[str] = None,
    grado: Optional[str] = None,
    nivel_lectura: Optional[str] = None,
    estado: Optional[str] = None,
    datos: Optional[dict] = Body(default=None)
):
    coleccion_est = db["estudiantes"]
    
    d_nombre = nombre or (datos.get("nombre") if datos else "Sin nombre")
    d_matricula = matricula or (datos.get("matricula") if datos else "S/N")
    d_grado = grado or (datos.get("grado") if datos else "S/G")
    d_nivel = nivel_lectura or (datos.get("nivel_lectura") if datos else "Básico")
    d_estado = estado or (datos.get("estado") if datos else "Activo")

    nuevo_doc = {
        "nombre": d_nombre,
        "matricula": d_matricula,
        "grado": d_grado,
        "nivel_inicial_lectura": d_nivel,
        "estado": d_estado,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    resultado = coleccion_est.insert_one(nuevo_doc)
    return {
        "mensaje": "Estudiante registrado correctamente",
        "id": str(resultado.inserted_id)
    }

@app.put("/actualizar-estudiante/{estudiante_id}")
async def actualizar_estudiante(
    estudiante_id: str,
    nombre: Optional[str] = None,
    matricula: Optional[str] = None,
    grado: Optional[str] = None,
    nivel_lectura: Optional[str] = None,
    estado: Optional[str] = None,
    datos: Optional[dict] = Body(default=None)
):
    coleccion_est = db["estudiantes"]
    try:
        obj_id = ObjectId(estudiante_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    d_nombre = nombre or (datos.get("nombre") if datos else None)
    d_matricula = matricula or (datos.get("matricula") if datos else None)
    d_grado = grado or (datos.get("grado") if datos else None)
    d_nivel = nivel_lectura or (datos.get("nivel_lectura") if datos else None)
    d_estado = estado or (datos.get("estado") if datos else None)

    actualizacion = {}
    if d_nombre: actualizacion["nombre"] = d_nombre
    if d_matricula: actualizacion["matricula"] = d_matricula
    if d_grado: actualizacion["grado"] = d_grado
    if d_nivel: actualizacion["nivel_inicial_lectura"] = d_nivel
    if d_estado: actualizacion["estado"] = d_estado

    if not actualizacion:
        return {"mensaje": "No hay datos para actualizar"}

    resultado = coleccion_est.update_one({"_id": obj_id}, {"$set": actualizacion})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    
    return {"mensaje": "Estudiante actualizado correctamente"}

@app.delete("/eliminar-estudiante/{estudiante_id}")
async def eliminar_estudiante(estudiante_id: str):
    coleccion_est = db["estudiantes"]
    try:
        obj_id = ObjectId(estudiante_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

    resultado = coleccion_est.delete_one({"_id": obj_id})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
        
    return {"mensaje": "Estudiante eliminado correctamente"}

# Ruta para el Ping (Health Check)
@app.get("/estado-servidor")
async def estado_servidor():
    try:
        db.command({"ping": 1})
        return {"estado": "En línea", "mensaje": "Conexión a Atlas exitosa"}
    except Exception as e:
        return {"estado": "Caído", "error": str(e)}