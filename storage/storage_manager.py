"""Storage manager for handling link storage operations."""

import json
import logging
import os
from typing import List, Dict, Optional
from threading import Lock

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class StorageManager:
    """Manages JSON-based storage for Telegram links."""
    
    def __init__(self, storage_path: str = "data/valid_links.json"):
        """Initialize storage manager."""
        self.storage_path = storage_path
        self.lock = Lock()  # For thread-safe file operations
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage file and directory if they don't exist."""
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, 'w') as f:
                json.dump({}, f)
    
    def _read_storage(self) -> Dict:
        """Read the current storage content."""
        try:
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Corrupted storage file, resetting to empty state")
            return {}
        except Exception as e:
            logger.error(f"Error reading storage: {e}")
            return {}
    
    def _write_storage(self, data: Dict):
        """Write data to storage."""
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing to storage: {e}")
            raise
    
    def store_links(self, user_id: str, username: str, links: List[str]) -> bool:
        """Store valid links for a user."""
        if not links:
            return True
            
        with self.lock:
            try:
                storage = self._read_storage()
                
                # Update or create user entry
                if user_id not in storage:
                    storage[user_id] = {
                        "username": username,
                        "links": []
                    }
                
                # Update username if changed
                storage[user_id]["username"] = username
                
                # Add new links (avoid duplicates)
                existing_links = set(storage[user_id]["links"])
                new_links = set(links)
                storage[user_id]["links"] = list(existing_links | new_links)
                
                self._write_storage(storage)
                return True
            except Exception as e:
                logger.error(f"Error storing links for user {user_id}: {e}")
                return False
    
    def get_user_links(self, user_id: str) -> Optional[Dict]:
        """Get all links for a specific user."""
        with self.lock:
            try:
                storage = self._read_storage()
                return storage.get(user_id)
            except Exception as e:
                logger.error(f"Error retrieving links for user {user_id}: {e}")
                return None
    
    def remove_link(self, user_id: str, link: str) -> bool:
        """Remove a specific link for a user."""
        with self.lock:
            try:
                storage = self._read_storage()
                if user_id not in storage:
                    return False
                
                if link in storage[user_id]["links"]:
                    storage[user_id]["links"].remove(link)
                    self._write_storage(storage)
                return True
            except Exception as e:
                logger.error(f"Error removing link for user {user_id}: {e}")
                return False
    
    def clear_user_links(self, user_id: str) -> bool:
        """Clear all links for a specific user."""
        with self.lock:
            try:
                storage = self._read_storage()
                if user_id in storage:
                    storage[user_id]["links"] = []
                    self._write_storage(storage)
                return True
            except Exception as e:
                logger.error(f"Error clearing links for user {user_id}: {e}")
                return False 