"""Configuration for the Personal Telegram File Locker Bot.

Secrets are read only from the runtime environment. Never add token or
database credentials as source-code defaults.
"""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
MONGO_URI = os.getenv("MONGO_URI", "").strip()
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "file_locker").strip()
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

_archive_chat_id = os.getenv("IMPORT_ARCHIVE_CHAT_ID", "").strip()
IMPORT_ARCHIVE_CHAT_ID = int(_archive_chat_id) if _archive_chat_id else None

PAGE_SIZE = 10

# Incoming files are processed by one FIFO worker to bound work on small hosts.
INGEST_QUEUE_MAXSIZE = 500
MAX_CONCURRENT_UPDATES = 8
INGEST_BASE_DELAY = 0.05
INGEST_PRESSURE_DELAY = 0.25
INGEST_HIGH_PRESSURE_DELAY = 0.75
INGEST_MEMORY_WARNING_RATIO = 0.82
INGEST_MEMORY_CRITICAL_RATIO = 0.90
INGEST_CPU_THROTTLE_WARNING_RATIO = 0.25
INGEST_PROGRESS_EDIT_INTERVAL = 1.5
INGEST_BATCH_IDLE_SECONDS = 3.0

# Old-message imports are sequential Bot API forwards, never a history scan.
LINKED_HISTORY_IMPORT_MAX_IDS = 500
LINKED_HISTORY_IMPORT_PROGRESS_EVERY = 25
LINKED_HISTORY_IMPORT_DELAY = 1.0
LINKED_HISTORY_IMPORT_MAX_RETRIES = 10

MIN_PASSWORD_LENGTH = 6

_raw_allowed = os.getenv("ALLOWED_CHAT_IDS", "")
ALLOWED_CHAT_IDS: set[int] = {
    int(chat_id.strip())
    for chat_id in _raw_allowed.split(",")
    if chat_id.strip()
}

# Telegram still enforces server-side flood limits. These values pace work
# and honour RetryAfter responses; they do not attempt to bypass limits.
BULK_CHUNK_SIZE = 10
BULK_SEND_DELAY = 0.8
BULK_PROGRESS_EVERY = 3
BULK_MAX_RETRIES = 5

# Telegram Stars are the payment method for digital services inside Telegram.
PREMIUM_MONTHLY_PRICE_STARS = int(
    os.getenv("PREMIUM_MONTHLY_PRICE_STARS", "100")
)
PREMIUM_SUBSCRIPTION_PERIOD_SECONDS = 30 * 24 * 60 * 60
SHAREABLE_CATEGORIES = {"videos", "archives"}

BOT_COMMANDS: list[tuple[str, str]] = [
    ("start", "Open your file locker"),
    ("drive", "Open your file locker"),
    ("stats", "Show storage stats"),
    ("search", "Search files by name"),
    ("sections", "Browse your custom sections"),
    ("favourites", "View your starred files"),
    ("recent", "View recently accessed files"),
    ("premium", "Unlock Premium with Telegram Stars"),
    ("terms", "Read Premium terms"),
    ("paysupport", "Get payment support"),
    ("admin", "Admin panel — all users & stats (owner only)"),
    ("setcommands", "Re-register all commands with Telegram"),
    ("backup", "Manage backup sources (admin channels/groups)"),
    ("signup", "Create your account"),
    ("login", "Log in to your account"),
    ("logout", "Log out of the current session"),
    ("whoami", "Show your account info"),
]

CATEGORIES: dict[str, dict] = {
    "documents": {
        "label": "\U0001f4c4 Documents",
        "extensions": {
            "pdf", "doc", "docx", "txt", "rtf", "odt",
            "xls", "xlsx", "ppt", "pptx", "csv", "epub", "md",
        },
    },
    "archives": {
        "label": "\U0001f5c2 Archives",
        "extensions": {"zip", "rar", "7z", "tar", "gz", "bz2", "xz", "iso"},
    },
    "videos": {
        "label": "\U0001f3ac Videos",
        "extensions": {
            "mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "m4v", "3gp",
        },
    },
    "images": {
        "label": "\U0001f5bc Images",
        "extensions": {
            "jpg", "jpeg", "png", "gif", "bmp", "webp", "svg", "heic", "tiff",
        },
    },
    "others": {"label": "\U0001f4e6 Others", "extensions": set()},
}

CATEGORY_ORDER = ["documents", "archives", "videos", "images", "others"]


def classify_extension(extension: str) -> str:
    ext = extension.lower().lstrip(".")
    for key, meta in CATEGORIES.items():
        if key != "others" and ext in meta["extensions"]:
            return key
    return "others"
