"""Purchase order tracker for a stores department.

Places orders with suppliers, marks deliveries as received, notifies the
warehouse and cleans up fulfilled orders.
"""
import logging
import sqlite3


def create_connection():
    """Create an in-memory database with the orders table."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        "CREATE TABLE orders (id INTEGER PRIMARY KEY, supplier TEXT, "
        "item TEXT, quantity INTEGER, received INTEGER)"
    )
    return conn


def place_order(conn, supplier, item, quantity):
    """Insert a new, unreceived order and return its id."""
    cursor = conn.execute(
        "INSERT INTO orders (supplier, item, quantity, received) "
        "VALUES (?, ?, ?, 0)",
        (supplier, item, quantity),
    )
    return cursor.lastrowid


def mark_received(conn, order_id):
    """Mark the order with the given id as received."""
    conn.execute("UPDATE orders SET received = 1 WHERE id = ?", (order_id,))


def notify_warehouse(supplier):
    """Tell the warehouse that a delivery from a supplier is expected."""
    print("notifying warehouse about " + supplier)


def cleanup(conn):
    """Delete all orders that have been received."""
    try:
        conn.execute("DELETE FROM orders WHERE received = 1")
    except sqlite3.Error:
        logging.exception("cleanup failed")


def pending_count(conn):
    """Return the number of orders not yet received."""
    query = "SELECT COUNT(*) FROM orders WHERE received = 0"
    return conn.execute(query).fetchone()[0]


def main():
    """Run a short demonstration."""
    conn = create_connection()
    order_total = 0
    for supplier, item, quantity in (
        ("Acme Steel", "rods", 40),
        ("Bolt Co", "bolts", 500),
    ):
        place_order(conn, supplier, item, quantity)
        order_total += quantity
    mark_received(conn, 1)
    notify_warehouse("Acme")
    print(pending_count(conn), order_total)
    cleanup(conn)


if __name__ == "__main__":
    main()
