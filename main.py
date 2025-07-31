import json
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = '8342772726:AAHrav56POF-wxrTQHp4 E_1pYfQSIqXQqnQ'
ARCHIVO_USUARIOS = 'usuarios.json'

def cargar_usuarios():
    try:
        with open(ARCHIVO_USUARIOS, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def guardar_usuarios(usuarios):
    with open(ARCHIVO_USUARIOS, 'w') as f:
        json.dump(usuarios, f, indent=2)

async def nuevo_usuario(update: Update, context: ContextTypes.DEFAULT_TYPE):
    usuarios = cargar_usuarios()
    for miembro in update.message.new_chat_members:
        user_id = str(miembro.id)
        nombre = miembro.full_name
        if user_id not in usuarios:
            nuevo_id = len(usuarios) + 1
            usuarios[user_id] = {"id_personal": nuevo_id, "nombre": nombre}
            guardar_usuarios(usuarios)
            await update.message.reply_text(f"👋 Bienvenido {nombre}! Tu ID de registro es #{nuevo_id}")
        else:
            await update.message.reply_text(f"👋 Hola de nuevo {nombre}, ya estás registrado.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, nuevo_usuario))
    print("✅ Bot en funcionamiento...")
    app.run_polling()
