"""Storage manager for handling link storage operations."""

import json
import logging
import os
from typing import List, Dict, Optional, Set
from threading import Lock

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class StorageManager:
    """Manages JSON-based storage for Telegram proxy channels."""
    
    def __init__(self, 
                 user_storage_path: str = "data/user_links.json",
                 global_storage_path: str = "data/proxy_channels.json"):
        """Initialize storage manager with separate files for user links and global channel list."""
        self.user_storage_path = user_storage_path
        self.global_storage_path = global_storage_path
        self.lock = Lock()  # For thread-safe file operations
        self._ensure_storage_exists()
    
    def _ensure_storage_exists(self):
        """Create storage files and directory if they don't exist."""
        os.makedirs(os.path.dirname(self.user_storage_path), exist_ok=True)
        
        # Initialize user storage if it doesn't exist
        if not os.path.exists(self.user_storage_path):
            with open(self.user_storage_path, 'w') as f:
                json.dump({}, f)
        
        # Check if global channels file exists
        if not os.path.exists(self.global_storage_path):
            logger.warning(f"Global proxy channels file not found at {self.global_storage_path}")
    
    def _read_user_storage(self) -> Dict:
        """Read the user storage content."""
        try:
            with open(self.user_storage_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.error("Corrupted user storage file, resetting to empty state")
            return {}
        except Exception as e:
            logger.error(f"Error reading user storage: {e}")
            return {}
    
    def _read_global_storage(self) -> List[str]:
        """Read the global channel list (manually maintained)."""
        try:
            if not os.path.exists(self.global_storage_path):
                logger.warning("Global proxy channels file not found")
                return []
                
            with open(self.global_storage_path, 'r') as f:
                data = json.load(f)
                return data.get("channels", [])
        except json.JSONDecodeError:
            logger.error("Corrupted global storage file")
            return []
        except Exception as e:
            logger.error(f"Error reading global storage: {e}")
            return []
    
    def _write_user_storage(self, data: Dict):
        """Write data to user storage."""
        try:
            with open(self.user_storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing to user storage: {e}")
            raise
    
    def store_links(self, user_id: str, username: str, links: List[str]) -> bool:
        """Store valid links for a user."""
        if not links:
            return True
            
        with self.lock:
            try:
                # Update user storage only
                user_storage = self._read_user_storage()
                if user_id not in user_storage:
                    user_storage[user_id] = {
                        "username": username,
                        "links": []
                    }
                
                user_storage[user_id]["username"] = username
                existing_user_links = set(user_storage[user_id]["links"])
                new_user_links = set(links)
                user_storage[user_id]["links"] = list(existing_user_links | new_user_links)
                
                # Save user storage
                self._write_user_storage(user_storage)
                return True
            except Exception as e:
                logger.error(f"Error storing links for user {user_id}: {e}")
                return False
    
    def get_user_links(self, user_id: str) -> Optional[Dict]:
        """Get all links for a specific user."""
        with self.lock:
            try:
                storage = self._read_user_storage()
                return storage.get(user_id)
            except Exception as e:
                logger.error(f"Error retrieving links for user {user_id}: {e}")
                return None
    
    def get_all_channels(self) -> List[str]:
        """Get the global list of all proxy channels (manually maintained)."""
        with self.lock:
            return self._read_global_storage()
    
    def remove_link(self, user_id: str, link: str) -> bool:
        """Remove a specific link for a user."""
        with self.lock:
            try:
                user_storage = self._read_user_storage()
                if user_id not in user_storage:
                    return False
                
                if link in user_storage[user_id]["links"]:
                    user_storage[user_id]["links"].remove(link)
                    self._write_user_storage(user_storage)
                return True
            except Exception as e:
                logger.error(f"Error removing link for user {user_id}: {e}")
                return False
    
    def clear_user_links(self, user_id: str) -> bool:
        """Clear all links for a specific user."""
        with self.lock:
            try:
                user_storage = self._read_user_storage()
                if user_id in user_storage:
                    user_storage[user_id]["links"] = []
                    self._write_user_storage(user_storage)
                return True
            except Exception as e:
                logger.error(f"Error clearing links for user {user_id}: {e}")
                return False 