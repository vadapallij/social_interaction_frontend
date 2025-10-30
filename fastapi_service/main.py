from fastapi import FastAPI
import os
from dotenv import load_dotenv
import django
import sys
from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
import io, base64, pandas as pd, numpy as np, matplotlib.pyplot as plt
import pymysql
import jwt
from datetime import datetime, timezone
from matplotlib.patches import Patch
from passlib.hash import bcrypt
import traceback
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import binascii
import hashlib
from fastapi import HTTPException
from passlib.hash import bcrypt
# ======================================================
# CONFIGURE MYSQL CONNECTION (use your same SSH tunnel)
# ======================================================

app = FastAPI(title="CareWatch API")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
sys.path.append(BASE_DIR)
load_dotenv()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()
# =====================================================
# Database Configuration
# =====================================================
DB_DEFAULT = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("DB_PORT", 3307)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor,
}

DB_CAREWATCH = {
    "host": os.getenv("CARE_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("CARE_DB_PORT", 3307)),
    "user": os.getenv("CARE_DB_USER"),
    "password": os.getenv("CARE_DB_PASSWORD"),
    "database": os.getenv("CARE_DB_NAME"),
    "cursorclass": pymysql.cursors.DictCursor,
}


# =====================================================
# Test Root Endpoint
# =====================================================
@app.get("/")
def root():
    return {"message": "✅ FastAPI connected directly via PyMySQL"}

# =====================================================
# Proximity Data Endpoint
# =====================================================

SECRET_KEY = "supersecretkey"   # 🔒 change later
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60



# ✅ Allow frontend (React) to talk to backend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000",
    "http://localhost:8010",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def verify_django_password(password, encoded):
    """Verify plaintext password against Django's PBKDF2 hash"""
    try:
        algorithm, iterations, salt, stored_hash = encoded.split('$', 3)
        iterations = int(iterations)
        dk = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), iterations)
        calc_hash = binascii.b2a_base64(dk).decode('ascii').strip()
        return calc_hash == stored_hash
    except Exception:
        return False

class RegisterRequest(BaseModel):
    username: str
    first_name: str
    last_name: str
    password: str
    email: EmailStr

@app.post("/register")
def register_user(user: RegisterRequest):
    conn = pymysql.connect(**DB_DEFAULT)
    with conn.cursor() as cur:
        # Check if username already exists
        cur.execute("SELECT id FROM auth_user WHERE username=%s", (user.username,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="Username already exists")

        # Insert into auth_user (Django's user model)
        hashed_password = bcrypt.hash(user.password)
        cur.execute("""
            INSERT INTO auth_user (username, first_name, last_name, email, password, is_active, is_staff, is_superuser, date_joined)
            VALUES (%s, %s, %s, %s, %s, 1, 0, 0, NOW())
        """, (user.username, user.first_name, user.last_name, user.email, hashed_password))
        conn.commit()

        # Get the new user's ID
        cur.execute("SELECT id FROM auth_user WHERE username=%s", (user.username,))
        user_id = cur.fetchone()["id"]

        # Insert into guest_user table if exists
        try:
            cur.execute("""
                INSERT INTO guest_user (user_id, is_approved)
                VALUES (%s, %s)
            """, (user_id, False))
            conn.commit()
        except Exception:
            pass  # If no guest_user table, ignore

    conn.close()
    return {"message": "Registration successful! Please wait for admin approval."}

from django.contrib.auth.hashers import check_password

def verify_user(username: str, password: str):
    """Verify Django user's password"""
    conn = pymysql.connect(**DB_DEFAULT)
    with conn.cursor() as cur:
        cur.execute("SELECT username, password FROM auth_user WHERE username=%s", (username,))
        user = cur.fetchone()
    conn.close()

    if user and check_password(password, user["password"]):
        return True
    return False


def create_access_token(username: str):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": username, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    try:
        if not verify_user(username, password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token(username)
        return {"access_token": token, "token_type": "bearer", "username": username}

    except Exception as e:
        print("❌ LOGIN ERROR:", e)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/dashboard/families")
def get_families(current_user: str = Depends(get_current_user)):
    """
    Return all distinct family IDs from the care_watch_data database.
    Only accessible to logged-in users (requires valid JWT).
    """
    try:
        conn = pymysql.connect(**DB_CAREWATCH)
        with conn.cursor() as cur:
            cur.execute("SELECT DISTINCT family_id FROM families ORDER BY family_id;")
            results = [row["family_id"] for row in cur.fetchall()]
        conn.close()
        return JSONResponse(content={"families": results, "count": len(results)})

    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
        )

from fastapi import Query

@app.get("/proximity-data/")
def ProximityData(
    start_date: str = Query(..., description="Start date in YYYY-MM-DD"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD"),
    interval: str = Query("1H", description="Resampling interval (e.g., 1H, 30T, 1D)")
):
    plt.switch_backend("agg")

    DEVICE_MAC = "80:6F:B0:7B:7B:91"

    # Convert to UTC timestamps
    start_dt = datetime.strptime(start_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    end_dt = datetime.strptime(end_date, "%Y-%m-%d").replace(tzinfo=timezone.utc)

    # Connect to DB
    try:
        conn = pymysql.connect(**DB_CAREWATCH)
        with conn.cursor() as cur:
            query = """
            SELECT 
                p.id AS packet_id, p.family_id, p.device_mac, p.sample_at_ms,
                p.cvl_increment, r.station_alias, r.station_mac, r.rssi
            FROM proximity_data p
            JOIN rts_station_rssi r ON p.id = r.packet_id
            WHERE p.device_mac = %s
            AND p.sample_at_ms BETWEEN %s AND %s
            ORDER BY p.sample_at_ms ASC
            """
            cur.execute(
                query,
                (DEVICE_MAC, int(start_dt.timestamp() * 1000), int(end_dt.timestamp() * 1000)),
            )
            rows = cur.fetchall()
        conn.close()
    except Exception as e:
        print("❌ Database error:", e)
        return {"message": f"Database error: {str(e)}"}

    if not rows:
        return {"message": f"No data found between {start_date} and {end_date}."}

    df = pd.DataFrame(rows)
    df["sample_at_utc"] = pd.to_datetime(df["sample_at_ms"], unit="ms", utc=True)
    df = df.sort_values("sample_at_utc")

    df_grouped = (
        df.groupby(pd.Grouper(key="sample_at_utc", freq=interval))["cvl_increment"]
        .sum()
        .reset_index()
    )

    # --- Create plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_grouped["sample_at_utc"], df_grouped["cvl_increment"], color="steelblue")
    ax.set_title(f"CVL Increment from {start_date} to {end_date}")
    ax.set_xlabel("Time")
    ax.set_ylabel("CVL Increment")
    ax.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    plot_base64 = base64.b64encode(buf.read()).decode("utf-8")
    plt.close(fig)

    return {"plot_image": plot_base64, "message": "Plot generated successfully"}

