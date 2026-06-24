def extract_requirements(jd):

    must_have = []
    nice_to_have = []

    jd = jd.lower()

    if "java" in jd:
        must_have.append("Java")

    if "spring boot" in jd:
        must_have.append("Spring Boot")

    if "react" in jd:
        must_have.append("React")

    if "aws" in jd:
        nice_to_have.append("AWS")

    return {
        "must_have": must_have,
        "nice_to_have": nice_to_have
    }


def compare_candidates(candidates):

    result = []

    for candidate in candidates:
        result.append(
            f"{candidate['candidate']} : {candidate['score']}"
        )

    return "\n".join(result)


def generate_interview_questions(candidate_name):

    return [
        f"What Java projects have you worked on, {candidate_name}?",
        "Explain Spring Boot architecture.",
        "What are Microservices?",
        "How does AWS help in application deployment?"
    ]