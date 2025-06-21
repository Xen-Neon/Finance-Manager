import os
import shutil
from datetime import datetime

# Define paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'database', 'finance.db')

# Create backup directory if not exists
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')
os.makedirs(BACKUP_DIR, exist_ok=True)

# Format: finance_backup_2025-06-19_14-23-10.db
timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
backup_file = os.path.join(BACKUP_DIR, f'finance_backup_{timestamp}.db')

# Copy the database file
try:
    shutil.copy(DB_PATH, backup_file)
    print(f"✅ Backup successful: {backup_file}")
except Exception as e:
    print(f"❌ Backup failed: {e}")
