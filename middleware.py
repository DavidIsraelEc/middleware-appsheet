from flask import Flask, request, jsonify
import gspread
from google.oauth2.service_account import Credentials

# Configurar Flask
app = Flask(__name__)

# Autenticación con Google Sheets
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# ID de tu Google Sheet (pon tu ID aquí)
SHEET_ID = "1jxB-pDVRadGbDRlsWn1guxsfqad3JYN7acXSr0vjdxQ"
sheet_usuarios = client.open_by_key(SHEET_ID).worksheet("USUARIOS")
sheet_vehiculos = client.open_by_key(SHEET_ID).worksheet("VEHICULOS")
sheet_registros = client.open_by_key(SHEET_ID).worksheet("REGISTROS")

@app.route("/", methods=["GET"])
def home():
    return "Middleware funcionando 🚀"

# Ruta para recibir webhooks desde AppSheet
@app.route("/webhook", methods=["POST"])
def recibir_webhook():
    try:
        data = request.json
        tabla = data.get("tabla")
        datos = data.get("datos")

        if not tabla or not datos:
            return jsonify({"error": "Datos inválidos"}), 400

        # Insertar datos en la hoja correspondiente
        if tabla == "USUARIOS":
            sheet_usuarios.append_row([datos["ID_NOMBRE"], datos["NOMBRE"], datos["DIVISION"], datos["FOTO"]])
        elif tabla == "VEHICULOS":
            sheet_vehiculos.append_row([datos["ID_VEHICULO"], datos["VEHICULO"], datos["CALLSING"], datos["DIVISION"], datos["FOTO"]])
        elif tabla == "REGISTROS":
            sheet_registros.append_row([datos["ID_USUARIO"], datos["NOMBRE"], datos["DIVISION"], datos["CALLSING"], datos["FECHA"], datos["USO DE INSUMOS"]])

        return jsonify({"mensaje": "Datos recibidos correctamente"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar el servidor
if __name__ == "__main__":
    app.run(debug=True, port=5000)
