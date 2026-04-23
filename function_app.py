import azure.functions as func
import logging
import requests

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

BASE_API_URL = "https://api-churn-ia-fkeaczfhcdbycgfx.canadacentral-01.azurewebsites.net"

PREDICT_URL = f"{BASE_API_URL}/predict"
CHAT_URL = f"{BASE_API_URL}/chat"
PRODUCTOS_URL = f"{BASE_API_URL}/productos"


@app.route(route="evaluar_churn", methods=["POST"])
def evaluar_churn(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Evaluando churn por reclamo")

    try:
        data = req.get_json()
        rut = data.get("rut")
    except Exception:
        return func.HttpResponse("JSON invalido", status_code=400)

    if not rut:
        return func.HttpResponse("Falta el RUT", status_code=400)

    try:
        response = requests.post(
            PREDICT_URL,
            json={"rut": rut},
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
    except requests.RequestException as e:
        logging.error(f"Error llamando a la API de churn: {e}")
        return func.HttpResponse("Error al conectar con la API", status_code=502)

    return func.HttpResponse(
        response.text,
        status_code=response.status_code,
        mimetype="application/json",
    )


@app.route(route="chat_cliente", methods=["POST"])
def chat_cliente(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Atendiendo chat de cliente")

    try:
        data = req.get_json()
        rut = data.get("rut")
        mensaje = data.get("mensaje")
    except Exception:
        return func.HttpResponse("JSON invalido", status_code=400)

    if not rut:
        return func.HttpResponse("Falta el RUT", status_code=400)

    try:
        response = requests.post(
            CHAT_URL,
            json={
                "rut": rut,
                "mensaje": mensaje,
            },
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
    except requests.RequestException as e:
        logging.error(f"Error llamando a la API de chat: {e}")
        return func.HttpResponse("Error al conectar con la API", status_code=502)

    return func.HttpResponse(
        response.text,
        status_code=response.status_code,
        mimetype="application/json",
    )


@app.route(route="productos", methods=["GET"])
def productos(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Consultando productos disponibles")

    try:
        response = requests.get(
            PRODUCTOS_URL,
            headers={"Content-Type": "application/json"},
            timeout=30,
        )
    except requests.RequestException as e:
        logging.error(f"Error llamando a la API de productos: {e}")
        return func.HttpResponse("Error al conectar con la API", status_code=502)

    return func.HttpResponse(
        response.text,
        status_code=response.status_code,
        mimetype="application/json",
    )
