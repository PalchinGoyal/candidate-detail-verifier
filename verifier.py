import re, json
from datetime import datetime, timezone

_EMAIL = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w{2,}$", re.I)

def _v_text(v): return len(v.strip()) >= 3
def _v_email(v): return bool(_EMAIL.match(v.strip()))
def _v_number(v):
    try: float(v); return True
    except ValueError: return False
def _v_yesno(v): return v.strip().lower() in {"yes", "no"}

VALIDATORS = {
    "text": _v_text,
    "email": _v_email,
    "number": _v_number,
    "yesno": _v_yesno,
}

ERR_MSGS = {
    "text": "Must be at least 3 characters",
    "email": "Enter a valid email address (e.g., user@example.com)",
    "number": "Enter a valid number (integer or decimal)",
    "yesno": "Answer must be Yes or No",
    "options": "Select one of the allowed options",
}

DEFAULT_FIELD_TYPES = {
    "name": "text",
    "email": "email",
    "phone": "number",
    "available": "yesno",
    "skills": "text",
}

def validate_single(val, vtype, required=True):
    val = (val or "").strip()
    if not val:
        return (False, val, "This field is required") if required else (True, val, "")
    if vtype not in VALIDATORS:
        return True, val, ""
    ok = VALIDATORS[vtype](val)
    return (ok, val, "") if ok else (False, val, ERR_MSGS.get(vtype, "Invalid value"))

def run_verification(data, posted):
    corrected, errors = {}, {}

    for field, _ in data.get("fields", {}).items():
        vtype = DEFAULT_FIELD_TYPES.get(field, "text")
        ok, val, msg = validate_single(posted.get(field, ""), vtype)
        if ok:
            if vtype == "number" and val:
                val = float(val) if "." in val else int(val)
            corrected[field] = val
        else:
            errors[field] = msg

    for q in data.get("additionalQuestions", []):
        qid = q["id"]
        vtype = q.get("type", "text")
        req = q.get("required", False)
        ok, ans, msg = validate_single(posted.get(qid, ""), vtype, req)
        if ok and (ans or req):
            if vtype == "number":
                ans = float(ans) if "." in ans else int(ans)
            corrected[qid] = ans
        elif not ok:
            errors[qid] = msg

    verified = not errors
    output = {
        "sessionId": data.get("sessionId"),
        "verified": verified,
        "correctedData": corrected if verified else {},
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors": errors,
    }
    return output, verified
