from pinecone import Pinecone, ServerlessSpec, Index  # type: ignore
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, inspect

load_dotenv()


class Embeddings:
    def __init__(self) -> None:
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index_name = "test"  # os.getenv("PINECONE_INDEX_NAME") or "DEFAULT_INDEX"
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

    def __get_database_schema(self, connection_string: str) -> dict:
        engine = create_engine(connection_string)
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        schema_dict = {}
        for table in tables:
            columns = inspector.get_columns(table)
            column_names = [column["name"] for column in columns]
            schema_dict[table] = column_names

        return schema_dict

    def __embedding_exists(self, embedding_id: str) -> bool:
        # Implement this method to check if the embedding already exists in the index
        result = self.index.query(ids=[embedding_id])
        return len(result) > 0

    def __sanitize_id(self, id: str) -> str:
        # Remove or replace non-ASCII characters
        return id.encode("ascii", "ignore").decode("ascii")

    def __create_table_embedding(self) -> None:
        database_uri = os.getenv("DATABASE_URI") or ""
        tables = self.__get_database_schema(database_uri)

        for table, columns in tables.items():
            sanitized_table_id = self.__sanitize_id(table)
            if not self.__embedding_exists(sanitized_table_id):
                table_embedding = self.model.encode(table)
                self.index.upsert(
                    [
                        {
                            "id": sanitized_table_id,
                            "values": table_embedding.tolist(),
                            "metadata": {"type": "table", "name": table},
                        }
                    ]
                )

            for column in columns:
                sanitized_column_id = self.__sanitize_id(f"{table}.{column}")
                if not self.__embedding_exists(sanitized_column_id):
                    col_embedding = self.model.encode(column)
                    self.index.upsert(
                        [
                            {
                                "id": sanitized_column_id,
                                "values": col_embedding.tolist(),
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


test = Embeddings()
