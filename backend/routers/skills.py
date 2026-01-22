from fastapi import APIRouter, HTTPException
from database import get_db
from typing import List, Dict

router = APIRouter(prefix="/api", tags=["skills"])


@router.get("/skills")
async def get_skills() -> dict:
    """
    Fetch existing skills from the database.
    Groups by topic and skill_name with count of templates.
    
    Returns:
        Dictionary containing list of skills with topic, skill_name, and count
    """
    try:
        db = get_db()
        
        # Query all templates and group by topic and skill_name
        response = db.table('question_templates').select('topic, skill_name').execute()
        
        if not response.data:
            return {"skills": []}
        
        # Group and count skills
        skills_map = {}
        for row in response.data:
            topic = row.get('topic', '')
            skill_name = row.get('skill_name', '')
            key = f"{topic}:{skill_name}"
            
            if key in skills_map:
                skills_map[key]['count'] += 1
            else:
                skills_map[key] = {
                    'topic': topic,
                    'skill_name': skill_name,
                    'count': 1
                }
        
        # Convert to list and sort by topic, then skill_name
        skills_list = sorted(
            skills_map.values(),
            key=lambda x: (x['topic'], x['skill_name'])
        )
        
        return {"skills": skills_list}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch skills: {str(e)}")
