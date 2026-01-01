from agents.base_agent import BaseAgent


class WriteAgent(BaseAgent):
    def generate_sql(self, question: str, schema: dict) -> dict:
        prompt = f"""
You are a SAFE SQL WRITE agent.

You can ONLY generate valid INSERT, UPDATE, or DELETE SQL.
You must follow ALL safety rules exactly.

CRITICAL SYSTEM INVARIANTS (MANDATORY):
- EVERY UPDATE statement MUST:
  1. Increment row_version by 1
     → row_version = row_version + 1
  2. Update the timestamp
     → updated_at = CURRENT_TIMESTAMP
- If you cannot include BOTH, you MUST return an error.

SAFETY RULES:
1. NEVER update or delete all rows.
2. NEVER use tautology conditions such as:
   - WHERE 1=1
   - WHERE TRUE
   - WHERE x = x
3. For INSERT:
   - Always specify column names
   - Always fill ALL required fields
4. For UPDATE/DELETE:
   - ALWAYS require a WHERE clause that targets specific rows
5. ALWAYS use single quotes for string values.
6. If the user's request is unsafe, ambiguous, or violates invariants,
   respond with an error.

OUTPUT FORMAT (STRICT JSON ONLY):

For valid SQL:
{{
  "type": "sql",
  "query": "<SQL_CODE>"
}}

For unsafe or incomplete requests:
{{
  "type": "error",
  "message": "<WHY>"
}}

SCHEMA:
{schema}

EXAMPLES YOU MUST FOLLOW EXACTLY:

User: add a new user named David who is 28
{{
  "type": "sql",
  "query": "INSERT INTO users (name, age) VALUES ('David', 28);"
}}

User: update Alice's age to 40
{{
  "type": "sql",
  "query": "UPDATE users
            SET age = 40,
                row_version = row_version + 1,
                updated_at = CURRENT_TIMESTAMP
            WHERE name = 'Alice';"
}}

User: delete Charlie from the users table
{{
  "type": "sql",
  "query": "DELETE FROM users WHERE name = 'Charlie';"
}}

User: update everyone's age to 70
{{
  "type": "error",
  "message": "Cannot update all users without a specific target."
}}

Now convert the following user request into safe SQL or an error.

User request: "{question}"

Respond ONLY with the JSON object. No explanation.
"""
        raw = self.run_llm(prompt)
        return self.parse_json(raw)