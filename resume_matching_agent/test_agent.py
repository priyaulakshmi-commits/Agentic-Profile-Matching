from matching_agent import app

result = app.invoke(
    {
        "job_description":
            """
            Need Java Developer
            with Spring Boot.
            AWS preferred.
            """
    }
)

print(result["report"])