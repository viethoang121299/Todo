import os, subprocess, shutil
from datetime import datetime
import streamlit as st # Streamlit Cloud + Git (b6)
from pathlib import Path # Streamlit Cloud + Git (b6)

DB_FILE = "todo.db"
BACKUP_DIR = "backups"

def setup_rclone_config():
    # Cấu hình rclone trên Streamlit Cloud thông qua Secrets (b6)
    if "rclone" in st.secrets:
        config_dir = Path.home() / ".config" / "rclone"
        config_dir.mkdir(parents=True, exist_ok=True)
        config_file = config_dir / "rclone.conf"

        with open(config_file, "w") as f:
            f.write(st.secrets["rclone"]["conf"])


def restore_db():
    # setup_rclone_config() # Git + Streamlit Cloud (b6)

    if not os.path.exists(DB_FILE):
        print("Không tìm thấy Database local → Đang khôi phục từ Google Drive...")
        subprocess.run([
            "rclone",
            "copy",
            "gdrive:todo_app/todo.db",
            "."
        ])
        print("Khôi phục hoàn tất.")


def backup_db():
    # setup_rclone_config() # Git + Streamlit Cloud (b6)
    os.makedirs(BACKUP_DIR, exist_ok=True)

    # 1. Tạo file backup local real-time
    name = datetime.now().strftime("todo_%Y%m%d_%H%M%S.db")
    local_path = os.path.join(BACKUP_DIR, name)
    shutil.copy2(DB_FILE, local_path)

    # 2. Upload bản backup real-time và bản mới nhất lên Drive
    subprocess.run(["rclone", "copy", local_path, "gdrive:todo_app/backups"])
    subprocess.run(["rclone", "copyto", DB_FILE, "gdrive:todo_app/todo.db"])

    # 3. Dọn dẹp giữ lại 30 bản local
    cleanup_local()


def cleanup_local():
    files = sorted(os.listdir(BACKUP_DIR))
    while len(files) > 30:
        os.remove(os.path.join(BACKUP_DIR, files[0]))
        files.pop(0)