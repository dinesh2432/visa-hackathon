from langchain_core.prompts import PromptTemplate

DQ_PROMPT = PromptTemplate(
    input_variables=["metadata"],
    template="""
You are a data quality expert in the payments domain.

Given the extracted metadata of a dataset, do the following:
1. Identify key data quality issues across dimensions:
   - Completeness
   - Accuracy
   - Consistency
   - Validity
   - Timeliness
   - Uniqueness
   - Integrity
2. Provide a brief explanation for each issue in plain language.
3. Suggest 3 prioritized remediation actions.
4. Mention any regulatory or compliance risks if applicable.

Dataset Metadata:
{metadata}

Respond in a clear, structured format.
"""
)
