# Dynamic Question Template Builder

A web application for creating and managing dynamic math question templates using Python-based logic. Built with **FastAPI** (backend), **Supabase** (database), and **HTML/CSS/JS** (frontend).

## 🎯 Features

- **User Selection**: Predefined user system for tracking template creators
- **Skills Management**: View existing question templates organized by topic and skill
- **Template Creation**: Rich interface for creating question templates with:
  - Grade selection (1-10)
  - Topic and skill autocomplete
  - Auto-calculated format numbering
  - Python code editors with syntax highlighting (CodeMirror)
  - Live preview functionality
  - Type selection (MCQ, MAQ, Numerical Input, Text Input, True-or-False)
- **Sandboxed Execution**: Safe Python code execution with:
  - Restricted builtins (no file/network access)
  - Execution timeout (2 seconds)
  - Clear error reporting

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **Supabase**: PostgreSQL database with real-time capabilities
- **RestrictedPython**: Sandboxed Python execution
- **Uvicorn**: ASGI server

### Frontend
- **HTML5/CSS3/JavaScript**: Pure vanilla implementation
- **CodeMirror**: Code editor with Python syntax highlighting
- **Inter Font**: Modern typography

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase account and project
- Modern web browser

## 🚀 Setup Instructions

### 1. Database Setup

1. Create a new project in [Supabase](https://supabase.com)
2. Go to the SQL Editor
3. Run the SQL script from `database/schema.sql` to create the table and indexes
4. Note your project URL and API key (Settings → API)

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file (copy from .env.example)
cp ../.env.example ../.env

# Edit .env file with your Supabase credentials
# SUPABASE_URL=your-supabase-url
# SUPABASE_KEY=your-supabase-key
```

### 3. Frontend Setup

No build step required! The frontend uses vanilla HTML/CSS/JS.

### 4. Running the Application

**Start the Backend:**
```bash
cd backend
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

**Serve the Frontend:**

You can use any static file server. Options:

**Option 1 - Python HTTP Server:**
```bash
cd frontend
python -m http.server 5500
```

**Option 2 - VS Code Live Server:**
- Install "Live Server" extension
- Right-click `index.html` → "Open with Live Server"

**Option 3 - Node.js http-server:**
```bash
npm install -g http-server
cd frontend
http-server -p 5500
```

The frontend will be available at `http://localhost:5500`

## 📁 Project Structure

```
question_generation/
├── backend/
│   ├── main.py                 # FastAPI application entry
│   ├── config.py               # Environment configuration
│   ├── database.py             # Supabase client
│   ├── requirements.txt        # Python dependencies
│   ├── routers/
│   │   ├── users.py           # User endpoints
│   │   ├── skills.py          # Skills endpoints
│   │   ├── suggestions.py     # Autocomplete endpoints
│   │   ├── templates.py       # Template CRUD
│   │   └── preview.py         # Preview execution
│   └── services/
│       └── sandbox.py         # Python sandbox execution
├── frontend/
│   ├── index.html             # Landing page (user selection)
│   ├── skills.html            # Skills listing
│   ├── template.html          # Template creation
│   ├── css/
│   │   └── styles.css         # Styling
│   └── js/
│       ├── app.js             # Utilities & API client
│       ├── skills.js          # Skills page logic
│       └── template.js        # Template page logic
├── database/
│   └── schema.sql             # Database schema
├── .env.example               # Environment template
├── .gitignore
└── README.md
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/users` | Get predefined users |
| GET | `/api/skills` | Get existing skills |
| GET | `/api/topics/suggest?q={query}` | Topic autocomplete |
| GET | `/api/skills/suggest?topic={topic}&q={query}` | Skill autocomplete |
| GET | `/api/templates/next-format?topic={topic}&skill_name={skill}` | Calculate next format |
| POST | `/api/preview` | Execute and preview templates |
| POST | `/api/templates` | Save new template |
| GET | `/health` | Health check |

## 👥 Predefined Users

- Krishna
- Abhishek
- Naveen
- Pranav
- Devashri
- Abhinav
- Stanzin
- Ganadhitya
- Manasa
- Sathwik
- Prasidhvel
- Swati
- Murali
- Nitesh
- Mohana Krishna

## 🔒 Security Considerations

### Python Sandbox
The application uses `RestrictedPython` to safely execute user-written Python code:

- **Restricted Imports**: Only `random` and `math` modules are accessible
- **No File Access**: `open()` and file operations are blocked
- **No Network Access**: Network modules are unavailable
- **Timeout Enforcement**: Code execution limited to 2 seconds
- **Safe Builtins**: Only safe built-in functions are available

> ⚠️ **Note**: While RestrictedPython provides good security, sandboxing Python is inherently challenging. For production use, consider additional isolation layers (containers, separate processes, etc.).

## 🎨 Code Editor Examples

### Question Template Example:
```python
# Example: Simple addition question
import random

a = random.randint(1, 10)
b = random.randint(1, 10)

question = f"What is {a} + {b}?"
```

### Answer Template Example:
```python
# Example: Calculate the answer
import random

a = random.randint(1, 10)
b = random.randint(1, 10)

answer = a + b
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure `.env` file exists with correct Supabase credentials
- Check Python version: `python --version` (should be 3.8+)
- Verify all dependencies: `pip install -r requirements.txt`

### Frontend can't connect to backend
- Ensure backend is running on port 8000
- Check CORS settings in `.env` (BACKEND_CORS_ORIGINS)
- Verify API_BASE_URL in `frontend/js/app.js`

### Preview not working
- Check browser console for errors
- Verify Python code syntax
- Ensure both question and answer templates are filled

### Database errors
- Verify Supabase credentials in `.env`
- Ensure schema.sql has been executed
- Check Supabase project status

## 📝 Development Notes

- The frontend uses localStorage to maintain user selection across pages
- Format field auto-increments based on existing templates for the same topic + skill
- Templates are auto-injected with `module="Basic-skills"` and `category="Math"`
- CodeMirror uses the "material-darker" theme for consistency with the dark UI

## 🤝 Contributing

This is an internal tool for content creators. For questions or issues, contact the development team.

## 📄 License

Internal use only.
