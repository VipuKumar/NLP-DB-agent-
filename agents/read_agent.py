from agents.base_agent import BaseAgent


class ReadAgent(BaseAgent):
    def generate_sql(self, question: str, schema: dict) -> str:
        prompt=f"""
You are a READ-ONLY SQL agent.
Convert the user's question into a SQL SELECT query.

Rules:
- ALWAYS generate SELECT.
- NEVER use UPDATE, DELETE, INSERT, DROP, ALTER, or TRUNCATE.

Schema:
{schema}

Question: {question}
SQL:
"""
        sql_query=self.run_llm(prompt)
        return sql_query.strip()