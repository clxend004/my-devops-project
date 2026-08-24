import os
import uuid
import logging
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))

KYC_WEBHOOK_SECRET = os.getenv("KYC_WEBHOOK_SECRET")
if not KYC_WEBHOOK_SECRET:
    raise RuntimeError("KYC_WEBHOOK_SECRET is not configured")

# ---------------------------
# CREATE FOLDERS
# ---------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
LOG_DIR = os.path.join(BASE_DIR, "logs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# ---------------------------
# LOGGING (FILE + TERMINAL)
# ---------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | backend | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, "transactions.log")),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# ---------------------------
# FLASK APP
# ---------------------------
app = Flask(__name__)
CORS(app)

# ---------------------------
# MONGODB
# ---------------------------
client = MongoClient("mongodb://mongodb:27017/")
db = client["kyc_db"]

kyc_collection = db["kyc_logs"]
tx_collection = db["tx_logs"]

logger.info("Connected to MongoDB")

# ======================================================
# HOME
# ======================================================
@app.route("/")
def home():
    return jsonify({"message": "Backend running"}), 200


# ======================================================
# FILE SAVE HELPER
# ======================================================
def save_file(file):
    if not file:
        return None

    file_id = str(uuid.uuid4())

    original_name = os.path.basename(file.filename)
    filename = file_id + "_" + original_name

    filepath = os.path.join(UPLOAD_DIR, filename)

    file.save(filepath)

    logger.info("KYC file stored: reference=%s", file_id)

    return filename

# ======================================================
# ✅ KYC WEBHOOK (W5-T1 + W5-T2)
# ======================================================
@app.route("/webhook/kyc", methods=["POST", "GET"])
def kyc_handler():

    if request.method == "POST":
        provided_secret = request.headers.get("X-KYC-Webhook-Secret")

        if not provided_secret or provided_secret != KYC_WEBHOOK_SECRET:
            logger.warning("Rejected KYC webhook: invalid authentication")
            return jsonify({"error": "Unauthorized"}), 401
        
    # ✅ GET → FETCH ALL RECORDS (for demo)
    if request.method == "GET":
        records = list(kyc_collection.find())

        for r in records:
            r["_id"] = str(r["_id"])

        return jsonify(records), 200

    # ✅ POST → CREATE KYC
    try:
        data = request.get_json(silent=True)

        # 👉 JSON input
        if data:
            user_id = data.get("user_id")
            status = data.get("status")
            score = data.get("score")
            aadhar = data.get("aadhar")

            id_file = None
            selfie_file = None

        # 👉 form-data input
        else:
            user_id = request.form.get("user_id")
            status = request.form.get("status")
            score = request.form.get("score")
            aadhar = request.form.get("aadhar")

            id_file = request.files.get("id_proof")
            selfie_file = request.files.get("selfie")

        # ✅ VALIDATION
        if not user_id or not status or not score:
            return jsonify({"error": "Missing required fields"}), 400

        # ✅ SAVE FILES
        id_filename = save_file(id_file)
        selfie_filename = save_file(selfie_file)

        record = {
            "user_id": user_id,
            "status": status,
            "score": int(score),
            "id_proof_file": id_filename,
            "selfie_file": selfie_filename,
            "timestamp": datetime.utcnow().isoformat()
        }

        result = kyc_collection.insert_one(record)

        # ✅ FIX ObjectId
        record["_id"] = str(result.inserted_id)

        logger.info(
        "KYC CREATED: status=%s score=%s",
         status,
         score
        )

        return jsonify({
            "message": "KYC created successfully",
            "file_reference_id": record["_id"],
            "data": record
        }), 200

    except Exception as e:
        logger.exception("KYC webhook processing failed")
        return jsonify({"error": "Internal server error"}), 500


# ======================================================
# ✅ TRANSACTION LOGGING (W6-T1)
# ======================================================
@app.route("/transaction", methods=["POST"])
def create_transaction():
    try:
        data = request.get_json(force=True)

        wallet = data.get("wallet")
        status = data.get("status")
        event = data.get("event")

        if not wallet or not status or not event:
            return jsonify({"error": "Missing required fields"}), 400

        tx_data = {
            "tx_id": str(uuid.uuid4()),
            "wallet": wallet,
            "status": status,
            "event": event,
            "timestamp": datetime.utcnow().isoformat()
        }

        result = tx_collection.insert_one(tx_data)

        # ✅ FIX ObjectId
        tx_data["_id"] = str(result.inserted_id)

        logger.info(f"TX LOG: {tx_data}")

        return jsonify({
            "message": "Transaction logged",
            "data": tx_data
        }), 200

    except Exception as e:
        logger.error(str(e))
        return jsonify({"error": str(e)}), 500


# ======================================================
# GET ALL TRANSACTIONS
# ======================================================
@app.route("/transaction", methods=["GET"])
def get_transactions():
    data = list(tx_collection.find())

    for d in data:
        d["_id"] = str(d["_id"])

    return jsonify(data), 200


# ======================================================
# GET ONE TRANSACTION
# ======================================================
@app.route("/transaction/<tx_id>", methods=["GET"])
def get_one_transaction(tx_id):
    data = tx_collection.find_one({"tx_id": tx_id})

    if not data:
        return jsonify({"error": "Not found"}), 404

    data["_id"] = str(data["_id"])
    return jsonify(data), 200


# ======================================================
# RUN
# ======================================================
if __name__ == "__main__":
    logger.info("Server started")
    app.run(host="0.0.0.0", port=5000)