from embeddings import Embeddings

# 1. Query to get employee names and their positions
print(Embeddings().get_relevant_schema("List all employee names and positions."))
print("Expected Result: [{'type': 'table', 'name': 'employees'}]")
print("*" * 50)

# 2. Query about projects' start and end dates
print(
    Embeddings().get_relevant_schema(
        "What are the start and end dates for the projects?"
    )
)
print("Expected Result: [{'type': 'table', 'name': 'projects'}]")
print("*" * 50)

# 3. Query requesting invoices issued by clients
print(Embeddings().get_relevant_schema("List all invoices issued by clients."))
print(
    "Expected Result: [{'type': 'table', 'name': 'invoices'}, {'type': 'table', 'name': 'clients'}]"
)
print("*" * 50)

# 4. Query for meeting details including location
print(Embeddings().get_relevant_schema("Show meeting details including location."))
print("Expected Result: [{'type': 'table', 'name': 'meetings'}]")
print("*" * 50)

# 5. Query about salary information
print(Embeddings().get_relevant_schema("Provide salary details for employees."))
print(
    "Expected Result: [{'type': 'table', 'name': 'salaries'}, {'type': 'table', 'name': 'employees'}]"
)
print("*" * 50)

# 6. Query for employee feedback
print(Embeddings().get_relevant_schema("Get the feedback provided to employees."))
print(
    "Expected Result: [{'type': 'table', 'name': 'feedback'}, {'type': 'table', 'name': 'employees'}]"
)
print("*" * 50)

# 7. Query for details of tasks and their due dates
print(
    Embeddings().get_relevant_schema(
        "What are the details of tasks and their due dates?"
    )
)
print(
    "Expected Result: [{'type': 'table', 'name': 'tasks'}, {'type': 'table', 'name': 'projects'}]"
)
print("*" * 50)

# 8. Query about department names and associated employees
print(
    Embeddings().get_relevant_schema(
        "Find all department names and their associated employees."
    )
)
print(
    "Expected Result: [{'type': 'table', 'name': 'departments'}, {'type': 'table', 'name': 'employees'}]"
)
print("*" * 50)

# 9. Query for client contact information
print(Embeddings().get_relevant_schema("List contact information for clients."))
print("Expected Result: [{'type': 'table', 'name': 'clients'}]")
print("*" * 50)

# 10. Query about review ratings for employees
print(Embeddings().get_relevant_schema("Provide review ratings for employees."))
print(
    "Expected Result: [{'type': 'table', 'name': 'reviews'}, {'type': 'table', 'name': 'employees'}]"
)
