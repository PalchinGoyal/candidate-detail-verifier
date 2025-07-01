# Candidate Detail Verifier 🗂️

A lightweight **CLI + Flask web app** that verifies, corrects, and enriches candidate data stored in a JSON file.

- **CLI mode** – run entirely in the terminal  
- **Web UI** – drag‑and‑drop an `input.json`, edit fields, get real‑time validation feedback, and download `output.json`  
- **Dynamic rules** – validation logic is data‑driven and reusable in both modes

---

## 🚀 Quick Start

```bash
git clone https://github.com/<your-user>/candidate-verifier.git
cd candidate-verifier

# (optional) create virtual env
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### 1. Run the Web UI 🌐

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000), upload `input.json`, answer questions, and download `output.json`.

### 2. Run via CLI 🖥️

```bash
python verifier.py input.json output.json
```

— or omit the second argument and it will write `output.json` next to the input.

---

## 🎯 Development Approach

### Core Philosophy
The project follows a **"single source of truth"** principle where all validation logic, field definitions, and business rules are centralized and reusable across both CLI and web interfaces.

### Key Design Decisions

**1. Schema-Driven Validation**
- All field types, validation rules, and required constraints are defined declaratively
- The `additionalQuestions` array allows dynamic form generation without code changes
- Validation logic is data-driven, not hardcoded

**2. Dual Interface Architecture**
- **Shared Core**: `verifier.py` contains the validation engine used by both interfaces
- **CLI Mode**: Direct file processing for batch operations and automation
- **Web Mode**: Interactive UI with real-time feedback for user-friendly experience

**3. Progressive Enhancement Strategy**
- Forms work with basic HTML submission (no JavaScript required)
- JavaScript enhances the experience with real-time validation
- Graceful degradation ensures accessibility across all environments

**4. Session-Based Workflow**
- Each upload gets a unique session ID for isolated processing
- Stateful validation allows step-by-step correction
- Session data persists temporarily for multi-step verification process

---

## 🔣 Input / Output Formats

### `input.json`

```json
{
    "sessionId": "abc123",
    "fields": {
        "name": "Jon",
        "email": "jon123@",
        "phone": "12345",
        "available": "Y",
        "skills": ""
    },
    "additionalQuestions": [
        {
            "id": "noticePeriod",
            "questionText": "What is your notice period?",
            "type": "text",
            "required": true
        },
        {
            "id": "experience",
            "questionText": "How many years of experience do you have?",
            "type": "number",
            "required": false
        },
        {
            "id": "preferredLocation",
            "questionText": "Which location do you prefer to work from?",
            "type": "text",
            "required": false
        }
    ]
}
```

### `output.json`

```json
{
    "sessionId": "abc123",
    "verified": true,
    "correctedData": {
        "name": "Jon",
        "email": "jon123@gmail.com",
        "phone": "12345",
        "available": "yes",
        "skills": "nextjs",
        "noticePeriod": "one month",
        "experience": 4,
        "preferredLocation": "alwar"
    },
    "timestamp": "2025-06-30T19:36:37.423521+00:00"
}
```

---

## 🛠️ Validation Rules

| Field Type | Validation Rule | Example |
|------------|----------------|---------|
| `text` | At least 3 characters | "Jon" → valid |
| `email` | Valid email format | "jon123@" → "jon123@gmail.com" |
| `phone` | Valid phone number | "12345" → accepts as string |
| `number` | Numeric values only | "4" → 4 (integer) |
| `yesno` | Yes/No responses | "Y" → "yes" |

### Built-in Field Types

- **Basic fields**: `name`, `email`, `phone`, `available`, `skills`
- **Dynamic questions**: Defined in `additionalQuestions` array
- **Type validation**: `text`, `number`, `email`, `yesno`, `options`
- **Required fields**: Configurable per question

---

## 🖼️ Screenshots

Located in `docs/screenshots/`:

| Step | File Name | Description |
|------|-----------|-------------|
| Upload | `step1_upload.png` | Drag & drop JSON file |
| Verify | `step2_verify.png` | Real-time field validation |
| Summary | `step3_summary.png` | Download corrected data |

---

## 🏗️ Implementation Strategy

### Validation Engine Design
**Centralized Rule Processing**: Created a unified validation system that processes both static fields (`name`, `email`, `phone`) and dynamic questions from the JSON schema. This eliminates code duplication and ensures consistent validation across interfaces.

**Type-Based Validation**: Implemented a polymorphic validation system where each field type (`text`, `email`, `number`, `yesno`) has specific validation logic while sharing common patterns like required field checking.

### Real-Time Feedback Architecture
**Hybrid Validation Approach**: Built a system that validates both client-side (for immediate feedback) and server-side (for security), using the same validation rules through a `/api/validate` endpoint.

**Event-Driven UI Updates**: Used JavaScript event listeners on form inputs to trigger validation requests, providing instant visual feedback without full page reloads.

### Data Flow Strategy
**Immutable Input Preservation**: The original input JSON is never modified. Instead, corrections are stored separately in `correctedData`, maintaining an audit trail of what was changed.

**Stateful Session Management**: Each validation session maintains state server-side, allowing users to partially complete the form and return later, while keeping uploaded data secure and isolated.

### Flexibility Through Configuration
**JSON-Driven Form Generation**: The web interface dynamically generates form fields based on the `additionalQuestions` array, meaning new question types can be added without touching the frontend code.

**Extensible Validation Rules**: New field types can be added by extending the validation dictionary, making the system easily maintainable and scalable.

---

## 🔧 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Upload page |
| `POST` | `/upload` | Process uploaded JSON |
| `GET` | `/verify/<session_id>` | Verification form |
| `POST` | `/api/validate` | Real-time field validation |
| `POST` | `/submit/<session_id>` | Submit corrected data |
| `GET` | `/download/<session_id>` | Download output JSON |

---

## 🚦 Getting Started

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Prepare your input**: Create `input.json` with candidate data
4. **Choose your mode**:
   - **Web UI**: Run `python app.py` and visit localhost:5000
   - **CLI**: Run `python verifier.py input.json`
5. **Get results**: Download or view your verified `output.json`

---

## 📜 License

MIT License – free to use, fork, and improve. Contributions welcome!

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

For bugs and feature requests, please open an issue on GitHub.