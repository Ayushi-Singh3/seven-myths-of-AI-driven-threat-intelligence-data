import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

prompt = "The following is a public report on a cybersecurity incident. Based on this report, what should this organization's board of directors learn from this incident? Answer in one or two paragraphs.\n\n"

with open("version_a.txt", "r") as f:
    version_a = f.read()

with open("version_b.txt", "r") as f:
    version_b = f.read()

def run(document, version_label, run_number):
    response = client.chat.completions.create(
        model="gpt-4o",
        temperature=0,
        max_tokens=2000,
        messages=[
            {"role": "user", "content": prompt + document}
        ]
    )
    output = response.choices[0].message.content
    print(f"=== {version_label} Run {run_number} ===")
    print(output)
    print()
    return output

results = []
for i in range(1, 4):
    results.append(("Version A", i, run(version_a, "Version A", i)))
for i in range(1, 4):
    results.append(("Version B", i, run(version_b, "Version B", i)))

with open("experiment_results.txt", "w") as f:
    for label, num, text in results:
        f.write(f"=== {label} Run {num} ===\n{text}\n\n")

print("All runs saved to experiment_results.txt")