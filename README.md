# Invoking Heuristics and Biases to Elicit Irrational Choices of LLMs

## Abstract

Despite the remarkable performance of Large Language Models (LLMs), they remain vulnerable to jailbreak attacks that can compromise their safety mechanisms. Existing studies often rely on brute-force optimization or manual prompt design and fail to capture risks in real-world scenarios. To address this, we propose **ICRT**, a novel jailbreak framework inspired by human cognitive heuristics and biases. 

- **Simplicity Effect**: We apply _cognitive decomposition_ to break complex malicious goals into simpler sub-tasks, reducing prompt complexity.  
- **Relevance Bias**: We reorganize and prioritize sub-concepts to maximize semantic alignment with the attacker’s intent.  
- **Ranking-Based Evaluation**: We move beyond binary success/failure by aggregating pairwise harmfulness comparisons via Elo, HodgeRank, and Rank Centrality, producing a fine-grained metric of output risk.

Our experiments demonstrate that ICRT consistently bypasses mainstream LLM safety guards and yields highly actionable, high-risk content—offering both deeper insights into jailbreak vulnerabilities and guidance for stronger defenses.

![ICRT Method Overview](./image/method.png)

---

## Getting Started

Follow these steps to run the ICRT jailbreak pipeline using our prompt templates:

1. **Intent Recognition**  
   - **Prompt File:** `Intent_Recognition.txt`  
   - **Input:** User’s original malicious query  
   - **Output:**  
     ```json
     {
       "structural_intent": "<what to do>",
       "harmful_behavior": "<how to do it>"
     }
     ```

2. **Concept Decomposition**  
   - **Prompt File:** `Concept_Decomposition.txt`  
   - **Input:**  
     ```json
     {
       "structural_intent": "<...>",
       "harmful_behavior": "<...>",
       "num_sub_concepts": N
     }
     ```  
   - **Output:**  
     ```json
     {
       "sub_concepts": [
         "sub-concept 1",
         "...",
         "sub-concept N"
       ]
     }
     ```

3. **Safety Filtering**  
   - **Prompt File:** `safety_constraint.txt`  
   - **Input:**  
     ```json
     {
       "sub_concepts": [ ... ],
       "max_removals": M
     }
     ```  
   - **Output:**  
     ```json
     {
       "filtered_sub_concepts": [
         "sub-concept 1",
         "...",
         "sub-concept P"
       ]
     }
     ```

4. **Concept Reassembly**  
   - **Prompt File:** `Concept_Reassembly.txt`  
   - **Input:**  
     ```json
     {
       "intent_recognition_result": { ... },
       "decomposed_sub_concepts": [ ... ],
       "num_selected_concepts": K
     }
     ```  
   - **Output:**  
     ```json
     {
       "selected_sub_concepts": [
         "sub-concept A",
         "...",
         "sub-concept K"
       ]
     }
     ```

5. **Jailbreak Prompt Generation**  
   - Embed the `selected_sub_concepts` into your scenario template (e.g., role-play, hypothetical discussion).  
   - Send the final prompt to your target LLM to obtain the jailbreak response.

6. **Harmfulness Evaluation**  
   - **Prompt File:** `judge.txt`  
   - **Input (JSON or plain text):**  
     ```json
     {
       "prompt": "<original prompt>",
       "text_A": "<completion A>",
       "text_B": "<completion B>"
     }
     ```  
   - **Output:**  
     ```json
     {
       "judgment": "A" | "B"
     }
     ```
