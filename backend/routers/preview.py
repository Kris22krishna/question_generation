from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from services.sandbox import execute_code
from typing import Optional, Any

router = APIRouter(prefix="/api", tags=["preview"])


class PreviewRequest(BaseModel):
    """Schema for preview request."""
    question_template: str = Field(..., min_length=1, description="Python code for question")
    answer_template: str = Field(..., min_length=1, description="Python code for answer")
    type: str = Field(..., description="Question type for display purposes")


@router.post("/preview")
async def preview_template(request: PreviewRequest) -> dict:
    """
    Execute question and answer templates in sandbox and return results.
    
    Args:
        request: Preview request with question and answer templates
        
    Returns:
        Dictionary containing question, answer, and any errors
    """
    result = {
        "question": None,
        "answer": None,
        "error": None,
        "error_type": None
    }
    
    try:
        # Execute question template
        question_result = execute_code(request.question_template)
        
        if question_result['error']:
            result['error'] = f"Question Template Error: {question_result['error']}"
            result['error_type'] = question_result['error_type']
            return result
        
        result['question'] = question_result['result']
        
        # Execute answer template
        answer_result = execute_code(request.answer_template)
        
        if answer_result['error']:
            result['error'] = f"Answer Template Error: {answer_result['error']}"
            result['error_type'] = answer_result['error_type']
            return result
        
        result['answer'] = answer_result['result']
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Preview failed: {str(e)}")
