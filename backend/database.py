from supabase import create_client, Client
from config import settings


class Database:
    """Supabase database client wrapper."""
    
    def __init__(self):
        self._client: Client = None
    
    def get_client(self) -> Client:
        """Get the Supabase client instance."""
        if self._client is None:
            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
        return self._client


# Global database instance
db = Database()


def get_db() -> Client:
    """Dependency function to get database client."""
    return db.get_client()
