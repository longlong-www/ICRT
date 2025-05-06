# Invoking Heuristics and Biases to Elicit Irrational Choices of LLMs

## Abstract

Despite the remarkable performance of Large Language Models (LLMs), they remain vulnerable to jailbreak attacks, which can compromise their safety mechanisms. Existing studies often rely on brute-force optimization or manual design, failing to uncover potential risks in real-world scenarios. To address this, we propose a novel jailbreak attack framework, ICRT, inspired by heuristics and biases in human cognition. Leveraging the simplicity effect, we employ cognitive decomposition to reduce the complexity of malicious prompts. Simultaneously, relevance bias is utilized to reorganize prompts, enhancing semantic alignment and inducing harmful outputs effectively. Furthermore, we introduce a ranking-based harmfulness evaluation metric that surpasses the traditional binary success-or-failure paradigm by employing ranking aggregation methods such as Elo, HodgeRank, and Rank Centrality to comprehensively quantify the harmfulness of generated content. Experimental results show that our approach consistently bypasses mainstream LLMs' safety mechanisms and generates high-risk content, providing insights into jailbreak attack risks and contributing to stronger defense strategies

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
       "num_sub_concepts": "N"
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
       "sub_concepts": [
         "sub-concept 1",
         "sub-concept 2",
         "sub-concept 3",
         "..."
       ],
       "max_removals": "M"
     }
     ```  
   - **Output:**  
     ```json
     {
       "filtered_sub_concepts": [
         "sub-concept 1",
         "sub-concept 3",
         "..."
       ]
     }
     ```


4. **Concept Reassembly**  
   - **Prompt File:** `Concept_Reassembly.txt`  
   - **Input:**  
     ```json
     {
       "intent_recognition_result": "{ ... }",
       "decomposed_sub_concepts": "[ ... ]",
       "num_selected_concepts": "K"
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
       "text_A": "<completion A>",
       "text_B": "<completion B>"
     }
     ```  
   - **Output:**  
     ```json
     {
       "judgment":" "A" or "B" "
     }
     ```
