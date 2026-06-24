from rag_search import *

create_vector_store()

results = search_resumes(
    "Java Spring Boot AWS developer"
)

for result in results:
    print(result.metadata)
    print(result.page_content)
    print("--------------------")