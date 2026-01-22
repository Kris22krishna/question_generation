import json
import os
from typing import Any, Dict, List
from supabase import create_client, Client
from config import settings

class MockResponse:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data

class MockQueryBuilder:
    def __init__(self, table_name: str, db: 'MockDatabase'):
        self.table_name = table_name
        self.db = db
        self._data = []
        self._filters = []

    def insert(self, data: Dict[str, Any]) -> 'MockQueryBuilder':
        self._data = [data] if isinstance(data, dict) else data
        return self

    def select(self, columns: str) -> 'MockQueryBuilder':
        # Simple implementation supports '*' basically
        return self

    def eq(self, column: str, value: Any) -> 'MockQueryBuilder':
        self._filters.append(('eq', column, value))
        return self

    def ilike(self, column: str, value: str) -> 'MockQueryBuilder':
        self._filters.append(('ilike', column, value))
        return self

    def execute(self) -> MockResponse:
        full_data = self.db._load_table(self.table_name)
        
        # Handle Insert
        if self._data:
            full_data.extend(self._data)
            self.db._save_table(self.table_name, full_data)
            return MockResponse(self._data)
            
        # Handle Select
        results = full_data
        for filter_type, col, val in self._filters:
            if filter_type == 'eq':
                results = [row for row in results if row.get(col) == val]
            elif filter_type == 'ilike':
                # Handle % wildcard roughly
                clean_val = val.replace('%', '').lower()
                results = [
                    row for row in results 
                    if str(row.get(col, '')).lower().find(clean_val) != -1
                ]
            
        return MockResponse(results)

class MockClient:
    def __init__(self):
        self.db_file = "local_db.json"
        if not os.path.exists(self.db_file):
            with open(self.db_file, 'w') as f:
                json.dump({}, f)
    
    def _load_table(self, table_name: str) -> List[Dict[str, Any]]:
        try:
            with open(self.db_file, 'r') as f:
                data = json.load(f)
            return data.get(table_name, [])
        except Exception:
            return []

    def _save_table(self, table_name: str, table_data: List[Dict[str, Any]]):
        with open(self.db_file, 'r') as f:
            full_db = json.load(f)
        
        full_db[table_name] = table_data
        
        with open(self.db_file, 'w') as f:
            json.dump(full_db, f, indent=2)

    def table(self, table_name: str) -> MockQueryBuilder:
        return MockQueryBuilder(table_name, self)

class Database:
    """Database client wrapper handling both Supabase and Mock."""
    
    def __init__(self):
        self._client = None
    
    def get_client(self) -> Any:
        """Get the database client instance."""
        if self._client is None:
            print(f"DEBUG: SUPABASE_KEY loaded: '{settings.SUPABASE_KEY}'")
            # Check if key is valid/present
            if not settings.SUPABASE_KEY or settings.SUPABASE_KEY == "YOUR_SUPABASE_KEY":
                print("WARNING: Using Mock Database (local_db.json) because SUPABASE_KEY is missing.")
                self._client = MockClient()
            else:
                try:
                    self._client = create_client(
                        settings.SUPABASE_URL,
                        settings.SUPABASE_KEY
                    )
                except Exception as e:
                    print(f"ERROR: Failed to connect to Supabase: {e}. Falling back to Mock DB.")
                    self._client = MockClient()
                    
        return self._client


# Global database instance
db = Database()


def get_db() -> Any:
    """Dependency function to get database client."""
    return db.get_client()
