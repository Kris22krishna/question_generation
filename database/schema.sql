-- Create question_templates table
CREATE TABLE question_templates (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    module TEXT NOT NULL,
    category TEXT NOT NULL,
    grade INTEGER NOT NULL CHECK (grade >= 1 AND grade <= 10),
    topic TEXT NOT NULL,
    skill_name TEXT NOT NULL,  
    format INTEGER NOT NULL CHECK (format >= 1),
    type TEXT NOT NULL CHECK (type IN ('MCQ', 'MAQ', 'Numerical Input', 'Text Input', 'True-or-False')),
    question_template TEXT NOT NULL,
    answer_template TEXT NOT NULL,
    created_by TEXT NOT NULL,
    updated_by TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX idx_topic ON question_templates(topic);
CREATE INDEX idx_topic_skill ON question_templates(topic, skill_name);
CREATE INDEX idx_topic_skill_format ON question_templates(topic, skill_name, format);
CREATE INDEX idx_created_by ON question_templates(created_by);
CREATE INDEX idx_grade ON question_templates(grade);

-- Create unique constraint to prevent duplicate templates
CREATE UNIQUE INDEX unique_template ON question_templates(topic, skill_name, format);

-- Add comment to table
COMMENT ON TABLE question_templates IS 'Stores dynamic question templates with Python code for generation';
