from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse

app = FastAPI(title="Router Middleware Example")

# ==================================================
# 🧠 Fake user (імітація БД / токена)
# ==================================================

fake_user = {
    "is_logged_in": True,
    "email_verified": True,
    "is_admin": False,   # ← зміни на True щоб зайти
}

# ==================================================
# 🌍 PUBLIC ROUTER (БЕЗ middleware)
# ==================================================

public_router = APIRouter()

@public_router.get("/health")
def health_check():
    return {"status": "ok"}

# ==================================================
# 👑 ADMIN ROUTER (БЕЗ middleware)
# ==================================================

admin_router = APIRouter(prefix="/admin")

@admin_router.get("/dashboard")
def admin_dashboard():
    return {"message": "Welcome to admin dashboard"}

@admin_router.get("/users")
def admin_users():
    return {"users": ["Alice", "Bob"]}

# ==================================================
# 🧩 REAL MIDDLEWARE (тільки для /admin/*)
# ==================================================

@app.middleware("http")
async def admin_only_middleware(request: Request, call_next):
    """
    Middleware працює ТІЛЬКИ для /admin/*
    """

    if request.url.path.startswith("/admin"):

        # 1️⃣ Чи користувач залогінений
        if not fake_user["is_logged_in"]:
            return JSONResponse(
                status_code=401,
                content={"error": "User not logged in"}
            )

        # 2️⃣ Чи підтверджена пошта
        if not fake_user["email_verified"]:
            return JSONResponse(
                status_code=403,
                content={"error": "Email not verified"}
            )

        # 3️⃣ Чи адмін
        if not fake_user["is_admin"]:
            return JSONResponse(
                status_code=403,
                content={"error": "Admin access only"}
            )

    # ✅ якщо не /admin або всі перевірки пройшли
    return await call_next(request)

# ==================================================
# 🔗 Підключення router'ів
# ==================================================

app.include_router(public_router)
app.include_router(admin_router)
