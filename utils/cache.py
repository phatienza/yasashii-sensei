"""
Yasashii Sensei - Simple In-Memory Cache with TTL
No database required - uses Python dict with timestamps.
"""

import time
from typing import Any, Optional


class SimpleCache:
    """Simple in-memory cache with TTL (Time To Live) support."""
    
    def __init__(self):
        """Initialize empty cache."""
        self._cache = {}
        self._timestamps = {}
        self._ttls = {}
    
    def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """
        Store a value in cache with expiration time.
        
        Args:
            key: Cache key
            value: Value to store
            ttl: Time to live in seconds (default: 1 hour)
        """
        self._cache[key] = value
        self._timestamps[key] = time.time()
        self._ttls[key] = ttl
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from cache if not expired.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value if exists and not expired, None otherwise
        """
        if key not in self._cache:
            return None
        
        if self.is_expired(key):
            self.delete(key)
            return None
        
        return self._cache[key]
    
    def is_expired(self, key: str) -> bool:
        """
        Check if a cache entry has expired.
        
        Args:
            key: Cache key
            
        Returns:
            True if expired or doesn't exist, False otherwise
        """
        if key not in self._timestamps:
            return True
        
        elapsed = time.time() - self._timestamps[key]
        ttl = self._ttls.get(key, 3600)
        
        return elapsed > ttl
    
    def delete(self, key: str) -> None:
        """
        Delete a cache entry.
        
        Args:
            key: Cache key
        """
        self._cache.pop(key, None)
        self._timestamps.pop(key, None)
        self._ttls.pop(key, None)
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._timestamps.clear()
        self._ttls.clear()
    
    def cleanup_expired(self) -> int:
        """
        Remove all expired entries from cache.
        
        Returns:
            Number of entries removed
        """
        expired_keys = [key for key in self._cache.keys() if self.is_expired(key)]
        
        for key in expired_keys:
            self.delete(key)
        
        return len(expired_keys)
    
    def size(self) -> int:
        """
        Get number of entries in cache.
        
        Returns:
            Number of cache entries
        """
        return len(self._cache)
    
    def keys(self) -> list:
        """
        Get all cache keys.
        
        Returns:
            List of cache keys
        """
        return list(self._cache.keys())


# Global cache instance
cache = SimpleCache()

# Made with Bob
