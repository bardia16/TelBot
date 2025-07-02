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
        
        # Initialize global channel list if it doesn't exist
        if not os.path.exists(self.global_storage_path):
            with open(self.global_storage_path, 'w') as f:
                json.dump({"channels": []}, f)
    
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
        """Read the global channel list."""
        try:
            with open(self.global_storage_path, 'r') as f:
                data = json.load(f)
                return data.get("channels", [])
        except json.JSONDecodeError:
            logger.error("Corrupted global storage file, resetting to empty state")
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
    
    def _write_global_storage(self, channels: List[str]):
        """Write data to global storage."""
        try:
            with open(self.global_storage_path, 'w') as f:
                json.dump({"channels": channels}, f, indent=2)
        except Exception as e:
            logger.error(f"Error writing to global storage: {e}")
            raise
    
    def store_links(self, user_id: str, username: str, links: List[str]) -> bool:
        """Store valid links for a user and update global channel list."""
        if not links:
            return True
            
        with self.lock:
            try:
                # Update user storage
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
                
                # Update global channel list
                global_channels = set(self._read_global_storage())
                global_channels.update(links)
                
                # Save both storages
                self._write_user_storage(user_storage)
                self._write_global_storage(sorted(list(global_channels)))
                
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
        """Get the global list of all unique channels."""
        with self.lock:
            try:
                return self._read_global_storage()
            except Exception as e:
                logger.error(f"Error retrieving global channel list: {e}")
                return []
    
    def remove_link(self, user_id: str, link: str) -> bool:
        """Remove a specific link for a user."""
        with self.lock:
            try:
                # Remove from user storage
                user_storage = self._read_user_storage()
                if user_id not in user_storage:
                    return False
                
                if link in user_storage[user_id]["links"]:
                    user_storage[user_id]["links"].remove(link)
                    self._write_user_storage(user_storage)
                
                # Update global storage
                all_user_links: Set[str] = set()
                for user_data in user_storage.values():
                    all_user_links.update(user_data["links"])
                
                self._write_global_storage(sorted(list(all_user_links)))
                return True
            except Exception as e:
                logger.error(f"Error removing link for user {user_id}: {e}")
                return False
    
    def clear_user_links(self, user_id: str) -> bool:
        """Clear all links for a specific user and update global list."""
        with self.lock:
            try:
                # Clear user storage
                user_storage = self._read_user_storage()
                if user_id in user_storage:
                    user_storage[user_id]["links"] = []
                    self._write_user_storage(user_storage)
                
                # Update global storage
                all_user_links: Set[str] = set()
                for user_data in user_storage.values():
                    all_user_links.update(user_data["links"])
                
                self._write_global_storage(sorted(list(all_user_links)))
                return True
            except Exception as e:
                logger.error(f"Error clearing links for user {user_id}: {e}")
                return False 