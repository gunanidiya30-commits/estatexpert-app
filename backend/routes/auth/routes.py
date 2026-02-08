from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from backend.config import get_db_connection

auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    message = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "")

        if not name or not email or not password or not role:
            message = "All fields are required."
        else:
            conn = get_db_connection()
            cur = conn.cursor(dictionary=True)
            # Check for existing user by email
            cur.execute("SELECT id FROM users WHERE email = %s", (email,))
            existing_user = cur.fetchone()
            if existing_user:
                message = "Email already registered."
            else:
                hashed_password = generate_password_hash(password)
                try:
                    cur.execute(
                        "INSERT INTO users (name, email, password_hash, role) VALUES (%s, %s, %s, %s)",
                        (name, email, hashed_password, role)
                    )
                    conn.commit()
                    cur.close()
                    conn.close()
                    return redirect(url_for("core.home"))
                except Exception as e:
                    message = "An error occurred. Please try again."
                finally:
                    cur.close()
                    conn.close()
    return render_template("auth/register.html", message=message)
