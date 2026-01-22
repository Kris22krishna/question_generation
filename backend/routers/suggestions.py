from fastapi import APIRouter, HTTPException, Query
from database import get_db
from typing import List, Optional

router = APIRouter(prefix="/api", tags=["suggestions"])


@router.get("/topics/suggest")
async def suggest_topics(q: str = Query(..., min_length=1)) -> dict:
    """
    Get topic suggestions based on query string.
    Returns up to 5 matching topics.
    
    Args:
        q: Query string for topic search
        
    Returns:
        Dictionary containing list of matching topics
    """
    try:
        db = get_db()
        
        # Query topics with case-insensitive partial match
        # Note: Supabase uses PostgREST which supports ilike for case-insensitive matching
        response = db.table('question_templates')\
            .select('topic')\
            .ilike('topic', f'%{q}%')\
            .execute()
        
        if not response.data:
            return {"suggestions": []}
        
        # Get unique topics and limit to 5
        topics = list(set(row['topic'] for row in response.data if row.get('topic')))
        topics.sort()
        
        return {"suggestions": topics[:5]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch topic suggestions: {str(e)}")


@router.get("/skills/suggest")
async def suggest_skills(
    topic: str = Query(..., min_length=1),
    q: Optional[str] = Query(None, min_length=1)
) -> dict:
    """
    Get skill suggestions filtered by topic and optional query string.
    Returns up to 5 matching skills.
    
    Args:
        topic: Topic to filter skills by
        q: Optional query string for skill search
        
    Returns:
        Dictionary containing list of matching skill names
    """
    try:
        db = get_db()
        
        # Start with topic filter
        query = db.table('question_templates')\
            .select('skill_name')\
            .eq('topic', topic)
        
        # Add skill_name filter if query provided
        if q:
            query = query.ilike('skill_name', f'%{q}%')
        
        response = query.execute()
        
        if not response.data:
            return {"suggestions": []}
        
        # Get unique skill names and limit to 5
        skills = list(set(row['skill_name'] for row in response.data if row.get('skill_name')))
        skills.sort()
        
        return {"suggestions": skills[:5]}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch skill suggestions: {str(e)}")
