from pymongo import MongoClient

# Tu conexión
uri = "mongodb+srv://Antonio_Marceliano:SoldierMaggot45@cluster1.wlqnuf6.mongodb.net/?tls=True"
cliente = MongoClient(uri)
db = cliente["chatbot_rag"]

# Ejecutar comando nativo de MongoDB
respuesta = db.command({"ping": 1})
print("Comando nativo ejecutado con éxito. Estado del servidor:", respuesta)