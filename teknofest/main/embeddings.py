from pinecone import Pinecone, ServerlessSpec, Index  # type: ignore
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os

load_dotenv()


class Embeddings:
    def __init__(self) -> None:
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index_name = os.getenv("PINECONE_INDEX_NAME") or "DEFAULT_INDEX"
        self.index = self.__get_index(index_name=index_name, pc=self.pc)
        self.model = SentenceTransformer(os.getenv("EMBEDDING_MODEL"))
        self.__create_table_embedding()

    def __get_index(self, index_name: str, pc: Pinecone) -> Index:
        self.__create_index_if_not_exists(pc=pc, index_name=index_name)
        return pc.Index(index_name)

    def __create_index_if_not_exists(self, pc: Pinecone, index_name: str) -> None:
        if index_name not in pc.list_indexes().names():
            pc.create_index(
                name=index_name,
                dimension=int(os.getenv("EMBEDDING_DIM")) or 768,  # type: ignore
                metric="cosine",
                spec=ServerlessSpec(cloud="aws", region="us-east-1"),
            )

    ## FIXME: GET SQL TABLES DYNAMICALLY
    ## FIXME: DONT CREATE TABLE EMBEDDINGS EVERY TIME
    def __create_table_embedding(self) -> None:
        tables = {
            "employees": ["id", "name", "position", "department_id"],
            "departments": ["id", "name"],
            "projects": ["id", "name", "start_date", "end_date", "department_id"],
            "salaries": ["id", "employee_id", "amount", "payment_date"],
            "clients": ["id", "name", "contact_email", "phone_number"],
            "invoices": ["id", "client_id", "issue_date", "due_date", "amount"],
            "meetings": ["id", "title", "meeting_date", "location", "department_id"],
            "tasks": ["id", "project_id", "description", "assigned_to", "due_date"],
            "reviews": ["id", "employee_id", "review_date", "rating", "comments"],
            "feedback": ["id", "employee_id", "feedback_date", "feedback_text"],
            "events": ["id", "name", "event_date", "location", "department_id"],
            "trainings": ["id", "title", "training_date", "duration", "instructor"],
            "attendance": ["id", "employee_id", "date", "status"],
            "assets": ["id", "name", "description", "purchase_date", "department_id"],
            "contracts": ["id", "client_id", "start_date", "end_date", "details"],
            "bonuses": ["id", "employee_id", "amount", "date_awarded"],
            "promotions": ["id", "employee_id", "new_position", "promotion_date"],
            "vacations": ["id", "employee_id", "start_date", "end_date", "status"],
            "leaves": ["id", "employee_id", "leave_type", "start_date", "end_date"],
            "benefits": ["id", "employee_id", "benefit_type", "start_date", "end_date"],
            "complaints": ["id", "employee_id", "complaint_date", "description"],
            "equipment": ["id", "name", "department_id", "acquisition_date"],
            "shifts": ["id", "employee_id", "shift_date", "shift_start", "shift_end"],
            "evaluations": [
                "id",
                "employee_id",
                "evaluation_date",
                "score",
                "comments",
            ],
            "work_orders": ["id", "task_id", "employee_id", "start_date", "end_date"],
            "suppliers": [
                "id",
                "name",
                "contact_name",
                "contact_email",
                "phone_number",
            ],
            "orders": ["id", "supplier_id", "order_date", "delivery_date", "status"],
            "deliveries": ["id", "order_id", "delivery_date", "status"],
            "inventories": ["id", "product_id", "quantity", "last_updated"],
            "products": ["id", "name", "category", "price", "stock_quantity"],
            "categories": ["id", "name", "description"],
            "logs": ["id", "employee_id", "log_date", "activity"],
            "achievements": ["id", "employee_id", "achievement_date", "description"],
            "certifications": [
                "id",
                "employee_id",
                "certification_name",
                "date_awarded",
            ],
            "news": ["id", "title", "content", "publish_date", "author"],
            "policies": ["id", "name", "content", "effective_date", "department_id"],
            "campaigns": ["id", "name", "start_date", "end_date", "department_id"],
            "budgets": ["id", "department_id", "amount", "fiscal_year"],
            "strategies": ["id", "name", "description", "start_date", "end_date"],
            "reports": ["id", "title", "content", "report_date", "author"],
            "audits": ["id", "department_id", "audit_date", "auditor", "findings"],
        }

        for table, columns in tables.items():
            table_id = f"{table}"
            if not self.__embedding_exists(table_id):
                table_embedding = self.model.encode(table)
                self.index.upsert(
                    [
                        {
                            "id": table_id,
                            "values": table_embedding.tolist(),  # type: ignore
                            "metadata": {"type": "table", "name": table},
                        }
                    ]
                )

            for column in columns:
                column_id = f"{table}.{column}"
                if not self.__embedding_exists(column_id):
                    col_embedding = self.model.encode(column)
                    self.index.upsert(
                        [
                            {
                                "id": column_id,
                                "values": col_embedding.tolist(),  # type: ignore
                                "metadata": {
                                    "type": "column",
                                    "name": column,
                                    "table": table,
                                },
                            }
                        ]
                    )

    def __embedding_exists(self, item_id: str) -> bool:
        try:
            result = self.index.fetch(ids=[item_id])
            if result and "ids" in result:
                return item_id in result["ids"]
            return False
        except Exception as e:
            print(f"Error checking if embedding exists for {item_id}: {e}")
            return False

    def get_relevant_schema(self, query):
        query_embedding = self.model.encode(query).tolist()
        results = self.index.query(vector=query_embedding, top_k=5)
        relevant_tables = set()
        for match in results["matches"]:
            match_id = match["id"]
            match_parts = match_id.split(".")
            if len(match_parts) == 1:
                relevant_tables.add(match_parts[0])
            elif len(match_parts) == 2:
                if query.lower().find(match_parts[1]) != -1:
                    relevant_tables.add(match_parts[0])

        return [{"type": "table", "name": table} for table in relevant_tables]
