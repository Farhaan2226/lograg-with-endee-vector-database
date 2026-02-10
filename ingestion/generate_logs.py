import random
import json
from datetime import datetime, timedelta

OUTPUT_FILE = "synthetic_logs.json"
NUM_LOGS = 600

# ---------------- SOURCES ----------------

SOURCES = [
    ("application", "java"),
    ("container", "docker"),
    ("network", "nginx"),
    ("system", "syslog"),
    ("security", "windows"),
]

SERVICES = [
    "auth-service",
    "payment-service",
    "order-service",
    "inventory-service",
    "notification-service",
    "gateway",
    "user-profile",
]

COMPONENTS = [
    "AuthController",
    "PaymentProcessor",
    "OrderHandler",
    "DBClient",
    "CacheLayer",
    "HttpClient",
]

LEVELS = ["INFO", "WARN", "ERROR"]

ERROR_PATTERNS = [
    ("NullPointerException", "Attempted to call method on null object", ["code", "exception"]),
    ("IndexOutOfBoundsException", "Index out of bounds", ["code"]),
    ("OutOfMemoryError", "Container killed due to memory limit", ["oom", "container"]),
    ("TimeoutException", "Upstream request timed out", ["timeout", "network"]),
    ("SQLException", "Deadlock detected", ["db", "lock"]),
    ("IOException", "Connection reset by peer", ["io", "network"]),
    ("AuthenticationException", "JWT token expired", ["auth", "security"]),
    ("AccessDeniedException", "User lacks required role", ["auth", "security"]),
    ("502 Bad Gateway", "Upstream service unavailable", ["http", "gateway"]),
    ("DiskFailure", "No space left on device", ["disk", "infra"]),
]

INFO_MESSAGES = [
    "Service started successfully",
    "Processing request",
    "Health check passed",
    "Cache hit for key user_profile",
    "Background job completed",
]

WARN_MESSAGES = [
    "Retrying failed request",
    "Slow response detected",
    "Cache miss for key session_id",
    "Rate limit approaching threshold",
]

STACK_TRACES = [
    """java.lang.NullPointerException
at com.app.service.AuthService.login(AuthService.java:42)
at com.app.controller.AuthController.handle(AuthController.java:88)
""",
    """java.lang.OutOfMemoryError: Java heap space
at com.app.cache.CacheLayer.put(CacheLayer.java:120)
""",
    """java.sql.SQLException: Deadlock found
at com.mysql.jdbc.Driver.execute(Driver.java:56)
""",
]

# ---------------- HELPERS ----------------

def random_timestamp():
    start = datetime.now() - timedelta(days=7)
    return (start + timedelta(seconds=random.randint(0, 604800))).isoformat()

def random_host():
    return f"node-{random.randint(1,5)}"

# ---------------- GENERATION ----------------

logs = []

for _ in range(NUM_LOGS):

    level = random.choices(
        LEVELS, weights=[0.6, 0.25, 0.15], k=1
    )[0]

    service = random.choice(SERVICES)
    component = random.choice(COMPONENTS)
    source, layer = random.choice(SOURCES)

    message = ""
    stack = ""
    tags = []

    if level == "ERROR":
        error, detail, tags = random.choice(ERROR_PATTERNS)
        message = f"{error}: {detail}"
        stack = random.choice(STACK_TRACES) if "Exception" in error else ""

    elif level == "WARN":
        message = random.choice(WARN_MESSAGES)
        tags = ["warning"]

    else:
        message = random.choice(INFO_MESSAGES)
        tags = ["info"]

    log = {
        "timestamp": random_timestamp(),
        "source": source,
        "service": service,
        "component": component,
        "layer": layer,
        "level": level,
        "message": message,
        "stack": stack,
        "host": random_host(),
        "tags": tags,
    }

    logs.append(log)

# ---------------- WRITE VALID JSON ----------------

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(logs, f, indent=2)

print(f"✅ Generated {NUM_LOGS} diverse synthetic logs → {OUTPUT_FILE}")
