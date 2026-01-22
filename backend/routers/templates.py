from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from database import get_db
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api", tags=["templates"])


class TemplateCreate(BaseModel):
    """Schema for creating a new template."""
    grade: int = Field(..., ge=1, le=10, description="Grade level (1-10)")
    topic: str = Field(..., min_length=1, description="Topic name")
    skill_name: str = Field(..., min_length=1, description="Skill name")
    format: int = Field(..., ge=1, description="Format number")
    type: str = Field(..., description="Question type (MCQ, MAQ, etc.)")
    question_template: str = Field(..., min_length=1, description="Python code for question generation")
    answer_template: str = Field(..., min_length=1, description="Python code for answer generation")
    created_by: str = Field(..., min_length=1, description="Username of creator")
    updated_by: Optional[str] = Field(None, description="Username of last updater")


@router.get("/templates/next-format")
async def get_next_format(
    topic: str = Query(..., min_length=1),
    skill_name: str = Query(..., min_length=1, alias="skill_name")
) -> dict:
    """
    Calculate the next format number for a given topic and skill.
    
    Args:
        topic: Topic name
        skill_name: Skill name
        
    Returns:
        Dictionary containing the next format number
    """
    try:
        db = get_db()
        
        # Query existing templates with matching topic and skill_name
        response = db.table('question_templates')\
            .select('format')\
            .eq('topic', topic)\
            .eq('skill_name', skill_name)\
            .execute()
        
        if not response.data:
            # No existing templates, start at 1
            return {"next_format": 1}
        
        # Find max format and increment
        max_format = max(row['format'] for row in response.data)
        
        return {"next_format": max_format + 1}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to calculate next format: {str(e)}")


@router.post("/templates")
async def create_template(template: TemplateCreate) -> dict:
    """
    Create a new question template.
    Auto-injects module and category fields.
    
    Args:
        template: Template data
        
    Returns:
        Dictionary containing created template data
    """
    try:
        db = get_db()
        
        # Prepare template data with auto-injected fields
        template_data = {
            'module': 'Basic-skills',
            'category': 'Math',
            'grade': template.grade,
            'topic': template.topic,
            'skill_name': template.skill_name,
            'format': template.format,
            'type': template.type,
            'question_template': template.question_template,
            'answer_template': template.answer_template,
            'created_by': template.created_by,
            'updated_by': template.updated_by or template.created_by,
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Insert into database
        response = db.table('question_templates').insert(template_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to save template")
        
        return {
            "success": True,
            "message": "Template created successfully",
            "data": response.data[0]
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create template: {str(e)}")
