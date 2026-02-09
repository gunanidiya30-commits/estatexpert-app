from backend.config import get_db_connection
from datetime import datetime


def create_property(owner_id, data):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO properties
        (title, description, property_type, bhk, area_sqft,
         city, locality, price, status, owner_id)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,'draft',%s)
        """,
        (
            data["title"],
            data.get("description"),
            data["property_type"],
            data.get("bhk"),
            data.get("area_sqft"),
            data.get("city"),
            data.get("locality"),
            data["price"],
            owner_id
        )
    )

    property_id = cursor.lastrowid

    # Log initial price
    cursor.execute(
        "INSERT INTO price_history (property_id, price) VALUES (%s,%s)",
        (property_id, data["price"])
    )

    conn.commit()
    cursor.close()
    conn.close()

    return property_id


def update_property(property_id, owner_id, data):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT owner_id, price FROM properties WHERE id = %s",
        (property_id,)
    )
    property_row = cursor.fetchone()

    if not property_row or property_row["owner_id"] != owner_id:
        cursor.close()
        conn.close()
        raise PermissionError("Unauthorized property update")

    cursor.execute(
        """
        UPDATE properties SET
        title=%s, description=%s, bhk=%s, area_sqft=%s,
        city=%s, locality=%s, price=%s
        WHERE id=%s
        """,
        (
            data["title"],
            data.get("description"),
            data.get("bhk"),
            data.get("area_sqft"),
            data.get("city"),
            data.get("locality"),
            data["price"],
            property_id
        )
    )

    if data["price"] != property_row["price"]:
        cursor.execute(
            "INSERT INTO price_history (property_id, price) VALUES (%s,%s)",
            (property_id, data["price"])
        )

    conn.commit()
    cursor.close()
    conn.close()


def publish_property(property_id, owner_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT status, owner_id FROM properties WHERE id=%s",
        (property_id,)
    )
    row = cursor.fetchone()

    if not row or row["owner_id"] != owner_id:
        cursor.close()
        conn.close()
        raise PermissionError("Unauthorized publish attempt")

    cursor.execute(
        """
        UPDATE properties SET status='active'
        WHERE id=%s
        """,
        (property_id,)
    )

    cursor.execute(
        """
        INSERT INTO property_status_log
        (property_id, old_status, new_status)
        VALUES (%s,%s,'active')
        """,
        (property_id, row["status"])
    )

    conn.commit()
    cursor.close()
    conn.close()
